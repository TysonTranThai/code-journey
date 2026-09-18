#!/usr/bin/env python3
"""Module 5 practices: inference, unions, generics, boundaries, ts-client."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "typescript-essentials"

# ── inference-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "inference-practice",
    "Shapes & Inference — Practice",
    "Think in shapes: build objects that satisfy contracts, normalize messy data, and apply utility-type logic at runtime.",
    "Hình dạng & Suy diễn — Luyện tập",
    "Tư duy theo hình dạng: dựng object thỏa mãn hợp đồng, chuẩn hóa dữ liệu lộn xộn, và áp dụng logic utility-type lúc runtime.",
    "why-types", 15, "intermediate",
    [
        {
            "id": "i2-shape-guard",
            "title": "Shape Checker",
            "prompt": "Write `hasShape(obj, spec)` — `spec` maps field names to expected typeof strings (`\"string\"`, `\"number\"`, `\"boolean\"`). RETURN true only when `obj` is a non-null object and every spec field exists with the exact typeof. Extra fields on `obj` are allowed (structural typing).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function hasShape(obj, spec) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "accepts objects matching the spec",
                    "code": fn_wrap("hasShape", "hasShape") + "\nconst spec = { id: \"string\", qty: \"number\" };\nif (hasShape({ id: \"a\", qty: 2 }, spec) !== true) throw new Error(\"Exact match accepted.\");\nif (hasShape({ id: \"a\", qty: 2, extra: true }, spec) !== true) throw new Error(\"Structural typing: extra fields allowed.\");",
                    "hint": "Every structural check passes with extra properties — that IS structural typing.",
                },
                {
                    "name": "rejects wrong types and missing fields",
                    "code": fn_wrap("hasShape", "hasShape") + "\nconst spec = { id: \"string\", qty: \"number\" };\nif (hasShape({ id: 7, qty: 2 }, spec) !== false) throw new Error(\"Wrong typeof fails.\");\nif (hasShape({ id: \"a\" }, spec) !== false) throw new Error(\"Missing fields fail.\");\nif (hasShape(null, spec) !== false) throw new Error(\"null is not an object here.\");\nif (hasShape(\"nope\", spec) !== false) throw new Error(\"Non-objects fail.\");",
                    "hint": "Guard typeof obj === 'object' && obj !== null first, then every [k, t] of Object.entries(spec).",
                },
            ],
        },
        {
            "id": "i2-normalize",
            "title": "Messy Data Normalizer",
            "prompt": "Write `normalizeUsers(raw)` — `raw` is an array of anything. Keep only entries that are objects with string `name` and a numeric `age` (Number(value) finite). RETURN normalized objects `{ name: trimmedName, age: number }`, dropping invalid entries silently.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function normalizeUsers(raw) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "keeps and normalizes valid entries",
                    "code": fn_wrap("normalizeUsers", "normalizeUsers") + "\nconst out = normalizeUsers([\n  { name: \"  Ada \", age: \"36\" },\n  { name: \"Bo\", age: 21 },\n]);\nif (out.length !== 2) throw new Error(\"Both entries are valid.\");\nif (out[0].name !== \"Ada\" || out[0].age !== 36) throw new Error(\"Names are trimmed; numeric strings become numbers.\");",
                    "hint": "typeof r.name === 'string' && Number.isFinite(Number(r.age)).",
                },
                {
                    "name": "drops junk without throwing",
                    "code": fn_wrap("normalizeUsers", "normalizeUsers") + "\nconst out = normalizeUsers([null, 42, { name: \"X\" }, { name: \"Y\", age: \"abc\" }, { name: \"Z\", age: -3 }]);\nif (out.length !== 1 || out[0].name !== \"Z\") throw new Error(\"Only the finite-age entry survives — everything else is dropped.\");",
                    "hint": "Filter first with the same predicate, then map to the normalized shape.",
                },
            ],
        },
        {
            "id": "i2-omit-pick",
            "title": "Pick & Omit",
            "prompt": "Implement the runtime twins of the utility types: `pick(obj, keys)` returns only the listed keys that exist, and `omit(obj, keys)` returns everything except them. Neither may mutate `obj`; both return fresh objects.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function pick(obj, keys) {\n  // your code\n}\n\nfunction omit(obj, keys) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "pick keeps listed keys only",
                    "code": fn_wrap("pick, omit", "pick, omit") + "\nconst u = { id: 1, email: \"a\", password: \"x\" };\nconst pub = pick(u, [\"id\", \"email\"]);\nif (pub.id !== 1 || pub.password !== undefined) throw new Error(\"Only listed keys survive.\");\nif (u.password !== \"x\") throw new Error(\"The input must not be mutated.\");",
                    "hint": "Build a fresh object key by key.",
                },
                {
                    "name": "omit removes listed keys",
                    "code": fn_wrap("pick, omit", "pick, omit") + "\nconst u = { id: 1, email: \"a\", password: \"x\" };\nconst safe = omit(u, [\"password\"]);\nif (safe.password !== undefined || safe.email !== \"a\") throw new Error(\"Listed keys removed, rest survive.\");\nif (Object.keys(u).length !== 3) throw new Error(\"Input untouched.\");\nconst both = omit(pick(u, [\"id\", \"email\"]), [\"email\"]);\nif (both.id !== 1 || both.email !== undefined) throw new Error(\"The utilities compose.\");",
                    "hint": "Copy everything, then delete the listed keys from the copy.",
                },
            ],
        },
    ],
    {
        "i2-shape-guard": {
            "title": "Bộ kiểm tra hình dạng",
            "prompt": "Viết `hasShape(obj, spec)` — `spec` ánh xạ tên trường sang chuỗi typeof mong đợi (`\"string\"`, `\"number\"`, `\"boolean\"`). RETURN true chỉ khi `obj` là object khác null và mọi trường trong spec tồn tại với typeof chính xác. Các trường thừa trên `obj` được phép (structural typing).",
            "tests": [
                {"name": "chấp nhận object khớp spec", "hint": "Mọi phép kiểm tra cấu trúc đều vượt qua khi có thuộc tính thừa — đó CHÍNH là structural typing."},
                {"name": "từ chối sai kiểu và thiếu trường", "hint": "Chặn typeof obj === 'object' && obj !== null trước, rồi mỗi cặp [k, t] của Object.entries(spec)."},
            ],
        },
        "i2-normalize": {
            "title": "Bộ chuẩn hóa dữ liệu lộn xộn",
            "prompt": "Viết `normalizeUsers(raw)` — `raw` là mảng chứa bất cứ gì. Chỉ giữ các phần tử là object có `name` là chuỗi và `age` là số (Number(value) hữu hạn). RETURN các object chuẩn hóa `{ name: nameTrimmed, age: number }`, lặng lẽ bỏ các phần tử không hợp lệ.",
            "tests": [
                {"name": "giữ và chuẩn hóa các phần tử hợp lệ", "hint": "typeof r.name === 'string' && Number.isFinite(Number(r.age))."},
                {"name": "bỏ rác mà không crash", "hint": "Lọc trước bằng cùng vị từ, rồi map sang hình dạng đã chuẩn hóa."},
            ],
        },
        "i2-omit-pick": {
            "title": "Pick & Omit",
            "prompt": "Cài đặt bản runtime của các utility type: `pick(obj, keys)` trả về chỉ các key được liệt kê và tồn tại, còn `omit(obj, keys)` trả về tất cả trừ chúng. Không hàm được làm thay đổi `obj`; cả hai trả về object mới.",
            "tests": [
                {"name": "pick giữ đúng các key được liệt kê", "hint": "Dựng object mới, từng key một."},
                {"name": "omit bỏ các key được liệt kê", "hint": "Copy toàn bộ, rồi delete các key được liệt kê khỏi bản copy."},
            ],
        },
    },
    [
        ["i2-shape-guard", "function hasShape(obj, spec) {\n  if (typeof obj !== \"object\" || obj === null) return false;\n  return Object.entries(spec).every(([k, t]) => typeof obj[k] === t);\n}", "function hasShape(obj, spec) { return true; }"],
        ["i2-normalize", "function normalizeUsers(raw) {\n  const out = [];\n  for (const r of raw) {\n    if (r && typeof r === \"object\" && typeof r.name === \"string\") {\n      const age = Number(r.age);\n      if (Number.isFinite(age)) {\n        out.push({ name: r.name.trim(), age });\n      }\n    }\n  }\n  return out;\n}", "function normalizeUsers(raw) {\n  return raw.map((r) => ({ name: r.name, age: Number(r.age) }));\n}"],
        ["i2-omit-pick", "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}\nfunction omit(obj, keys) {\n  const out = { ...obj };\n  for (const k of keys) {\n    delete out[k];\n  }\n  return out;\n}", "function pick(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}\nfunction omit(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}"],
    ],
)

# ── unions-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "unions-practice",
    "Unions & Narrowing — Practice",
    "Runtime narrowing: typeof-based formatters, a discriminated-union reducer, and exhaustive switches with a default that throws.",
    "Union & Narrowing — Luyện tập",
    "Thu hẹp kiểu lúc runtime: formatter dựa trên typeof, reducer cho discriminated union, và switch đầy đủ với default ném lỗi.",
    "unions-narrowing", 18, "intermediate",
    [
        {
            "id": "i2-narrow-format",
            "title": "Narrowing Formatter",
            "prompt": "Write `format(value)` handling the union `string | number | boolean | null | undefined`: strings are trimmed then returned, numbers are formatted with exactly 2 decimals, booleans become `\"yes\"`/`\"no\"`, null/undefined become `\"—\"`.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function format(value) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "each union member formats correctly",
                    "code": fn_wrap("format", "format") + "\nif (format(\"  hi  \") !== \"hi\") throw new Error(\"Strings are trimmed.\");\nif (format(3.14159) !== \"3.14\") throw new Error(\"Numbers get two decimals.\");\nif (format(true) !== \"yes\" || format(false) !== \"no\") throw new Error(\"Booleans map to yes/no.\");\nif (format(null) !== \"—\" || format(undefined) !== \"—\") throw new Error(\"Nullish becomes a dash.\");",
                    "hint": "Check null/undefined first, then typeof for the rest.",
                },
                {
                    "name": "zero is a number, not falsy-nullish",
                    "code": fn_wrap("format", "format") + "\nif (format(0) !== \"0.00\") throw new Error(\"0 must format as a number — beware truthiness checks.\");\nif (format(\"\") !== \"\") throw new Error(\"Empty string is still a string (trimmed).\");",
                    "hint": "value === null || value === undefined — not !value.",
                },
            ],
        },
        {
            "id": "i2-union-reducer",
            "title": "Discriminated Reducer",
            "prompt": "Write `reduceRequest(state, action)` for a request state machine. State is `{ kind: \"idle\" } | { kind: \"loading\" } | { kind: \"success\", data } | { kind: \"error\", message }`. Actions: `{ type: \"start\" }` → loading; `{ type: \"resolve\", data }` → success; `{ type: \"reject\", message }` → error; `{ type: \"reset\" }` → idle. RETURN the new state; never mutate.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function reduceRequest(state, action) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "full lifecycle",
                    "code": fn_wrap("reduceRequest", "reduceRequest") + "\nlet s = { kind: \"idle\" };\ns = reduceRequest(s, { type: \"start\" });\nif (s.kind !== \"loading\") throw new Error(\"start → loading.\");\ns = reduceRequest(s, { type: \"resolve\", data: [1, 2] });\nif (s.kind !== \"success\" || s.data.join() !== \"1,2\") throw new Error(\"resolve → success with data.\");\ns = reduceRequest(s, { type: \"reject\", message: \"503\" });\nif (s.kind !== \"error\" || s.message !== \"503\") throw new Error(\"reject → error with message.\");\ns = reduceRequest(s, { type: \"reset\" });\nif (s.kind !== \"idle\") throw new Error(\"reset → idle.\");",
                    "hint": "switch on action.type returning fresh state objects.",
                },
                {
                    "name": "success state carries data only there",
                    "code": fn_wrap("reduceRequest", "reduceRequest") + "\nconst s = reduceRequest({ kind: \"idle\" }, { type: \"start\" });\nif (\"data\" in s) throw new Error(\"The loading state must not fabricate a data field — variants carry only their own fields.\");",
                    "hint": "Return { kind: 'loading' } exactly — no extra keys.",
                },
            ],
        },
        {
            "id": "i2-exhaustive",
            "title": "Exhaustive Switch",
            "prompt": "Write `describeShape(v)` where `v` is `null | string | number | boolean | array`. RETURN: `\"nothing\"` for null, `\"text\"` for strings, `\"number\"` for numbers, `\"flag\"` for booleans, `\"list of N\"` (with the length) for arrays, and for ANYTHING ELSE throw `new Error(\"Unhandled shape\")` — the runtime twin of the never-check.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function describeShape(v) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "known shapes map correctly",
                    "code": fn_wrap("describeShape", "describeShape") + "\nif (describeShape(null) !== \"nothing\") throw new Error(\"null → nothing.\");\nif (describeShape(\"x\") !== \"text\") throw new Error(\"string → text.\");\nif (describeShape(5) !== \"number\") throw new Error(\"number → number.\");\nif (describeShape(false) !== \"flag\") throw new Error(\"boolean → flag.\");\nif (describeShape([1, 2, 3]) !== \"list of 3\") throw new Error(\"array → list of N.\");",
                    "hint": "Array.isArray after the typeof checks.",
                },
                {
                    "name": "unknown shapes throw",
                    "code": fn_wrap("describeShape", "describeShape") + "\nlet threw = false;\ntry { describeShape({ surprise: true }); } catch { threw = true; }\nif (!threw) throw new Error(\"An unhandled shape must throw 'Unhandled shape' — the default case is not optional.\");",
                    "hint": "End with throw new Error('Unhandled shape') as the exhaustive fallback.",
                },
            ],
        },
    ],
    {
        "i2-narrow-format": {
            "title": "Formatter thu hẹp kiểu",
            "prompt": "Viết `format(value)` xử lý union `string | number | boolean | null | undefined`: chuỗi được trim rồi trả về, số được định dạng đúng 2 chữ số thập phân, boolean thành `\"yes\"`/`\"no\"`, null/undefined thành `\"—\"`.",
            "tests": [
                {"name": "mỗi thành viên union được định dạng đúng", "hint": "Kiểm tra null/undefined trước, rồi typeof cho phần còn lại."},
                {"name": "số 0 là số, không phải nullish", "hint": "value === null || value === undefined — đừng dùng !value."},
            ],
        },
        "i2-union-reducer": {
            "title": "Reducer dạng discriminated",
            "prompt": "Viết `reduceRequest(state, action)` cho máy trạng thái request. State là `{ kind: \"idle\" } | { kind: \"loading\" } | { kind: \"success\", data } | { kind: \"error\", message }`. Các action: `{ type: \"start\" }` → loading; `{ type: \"resolve\", data }` → success; `{ type: \"reject\", message }` → error; `{ type: \"reset\" }` → idle. RETURN trạng thái mới; không bao giờ đụng vào state cũ.",
            "tests": [
                {"name": "vòng đời đầy đủ", "hint": "switch theo action.type, trả về các object trạng thái mới."},
                {"name": "trạng thái success chỉ mang data tại đó", "hint": "Return { kind: 'loading' } chuẩn xác — không thêm key thừa."},
            ],
        },
        "i2-exhaustive": {
            "title": "Switch đầy đủ",
            "prompt": "Viết `describeShape(v)` trong đó `v` là `null | string | number | boolean | array`. RETURN: `\"nothing\"` cho null, `\"text\"` cho chuỗi, `\"number\"` cho số, `\"flag\"` cho boolean, `\"list of N\"` (kèm độ dài) cho mảng, và với MỌI THỨ KHÁC hãy throw `new Error(\"Unhandled shape\")` — bản runtime của phép kiểm tra never.",
            "tests": [
                {"name": "các hình dạng đã biết ánh xạ đúng", "hint": "Array.isArray sau các kiểm tra typeof."},
                {"name": "hình dạng lạ sẽ throw", "hint": "Kết thúc bằng throw new Error('Unhandled shape') làm fallback đầy đủ."},
            ],
        },
    },
    [
        ["i2-narrow-format", "function format(value) {\n  if (value === null || value === undefined) return \"—\";\n  if (typeof value === \"string\") return value.trim();\n  if (typeof value === \"number\") return value.toFixed(2);\n  if (typeof value === \"boolean\") return value ? \"yes\" : \"no\";\n  throw new Error(\"unreachable\");\n}", "function format(value) {\n  if (!value) return \"—\";\n  return String(value);\n}"],
        ["i2-union-reducer", "function reduceRequest(state, action) {\n  switch (action.type) {\n    case \"start\": return { kind: \"loading\" };\n    case \"resolve\": return { kind: \"success\", data: action.data };\n    case \"reject\": return { kind: \"error\", message: action.message };\n    case \"reset\": return { kind: \"idle\" };\n    default: return state;\n  }\n}", "function reduceRequest(state, action) {\n  state.kind = action.type;\n  return state;\n}"],
        ["i2-exhaustive", "function describeShape(v) {\n  if (v === null) return \"nothing\";\n  if (typeof v === \"string\") return \"text\";\n  if (typeof v === \"number\") return \"number\";\n  if (typeof v === \"boolean\") return \"flag\";\n  if (Array.isArray(v)) return \"list of \" + v.length;\n  throw new Error(\"Unhandled shape\");\n}", "function describeShape(v) {\n  return String(v);\n}"],
    ],
)

# ── generics-practice ───────────────────────────────────────────────────────
write_practice(
    MOD, "generics-practice",
    "Generics — Practice",
    "Shape-preserving functions: a first-or-default picker, a keyed group-by, and a result-wrapping combinator whose output shape mirrors its input.",
    "Generics — Luyện tập",
    "Hàm giữ nguyên hình dạng: bộ chọn first-or-default, group-by theo key, và combinator bọc kết quả có hình dạng đầu ra phản chiếu đầu vào.",
    "generics", 18, "intermediate",
    [
        {
            "id": "i2-first-or",
            "title": "First or Default",
            "prompt": "Write `firstOr(items, fallback)` — RETURN the first element or `fallback` when the list is empty. The RETURNED value must have the SAME type relationship as the input (works for any element kind, no coercion).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function firstOr(items, fallback) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "returns the first element for any kind",
                    "code": fn_wrap("firstOr", "firstOr") + "\nif (firstOr([\"a\", \"b\"], \"z\") !== \"a\") throw new Error(\"First string wins.\");\nif (firstOr([{ n: 1 }], { n: 0 }).n !== 1) throw new Error(\"Objects pass through untouched.\");\nif (firstOr([], 9) !== 9) throw new Error(\"Empty list yields the fallback.\");",
                    "hint": "items.length ? items[0] : fallback — nothing more.",
                },
            ],
        },
        {
            "id": "i2-group-by",
            "title": "Keyed Group-By",
            "prompt": "Write `groupBy(items, keyFn)` RETURNing an object mapping each key to the array of items with that key (order preserved within groups). Write `keyCount(groups)` that takes the result and returns the number of distinct keys.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function groupBy(items, keyFn) {\n  // your code\n}\n\nfunction keyCount(groups) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "groups preserve item order",
                    "code": fn_wrap("groupBy, keyCount", "groupBy, keyCount") + "\nconst items = [\n  { t: \"a\", kind: \"x\" }, { t: \"b\", kind: \"y\" },\n  { t: \"c\", kind: \"x\" }, { t: \"d\", kind: \"x\" },\n];\nconst g = groupBy(items, (i) => i.kind);\nif (g.x.map((i) => i.t).join() !== \"a,c,d\") throw new Error(\"Group x keeps insertion order.\");\nif (g.y.length !== 1) throw new Error(\"Group y holds one item.\");\nif (keyCount(g) !== 2) throw new Error(\"Two distinct keys.\");",
                    "hint": "Push into (acc[k] ??= []).push(item) while walking the array once.",
                },
                {
                    "name": "empty input yields empty groups",
                    "code": fn_wrap("groupBy, keyCount", "groupBy, keyCount") + "\nconst g = groupBy([], (i) => i);\nif (Object.keys(g).length !== 0 || keyCount(g) !== 0) throw new Error(\"No items, no keys.\");",
                    "hint": "The loop simply never runs.",
                },
            ],
        },
        {
            "id": "i2-result-wrap",
            "title": "Result Wrapper",
            "prompt": "Write `attempt(fn)` — calls zero-argument `fn`. On success RETURN `{ ok: true, value }`; on throw RETURN `{ ok: false, error: err.message }`. The value keeps whatever shape fn returned (number, array, object — anything), proving the wrapper is shape-agnostic.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function attempt(fn) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "wraps success and failure for any shape",
                    "code": fn_wrap("attempt", "attempt") + "\nconst a = attempt(() => [1, 2, 3]);\nif (a.ok !== true || a.value.join() !== \"1,2,3\") throw new Error(\"Arrays pass through inside ok.\");\nconst b = attempt(() => ({ deep: { x: 1 } }));\nif (b.value.deep.x !== 1) throw new Error(\"Objects pass through.\");\nconst c = attempt(() => { throw new Error(\"nope\"); });\nif (c.ok !== false || c.error !== \"nope\") throw new Error(\"Failures become { ok: false, error }.\");",
                    "hint": "try { return { ok: true, value: fn() }; } catch (err) { return { ok: false, error: err.message }; }",
                },
            ],
        },
    ],
    {
        "i2-first-or": {
            "title": "Phần tử đầu hoặc mặc định",
            "prompt": "Viết `firstOr(items, fallback)` — RETURN phần tử đầu tiên hoặc `fallback` khi danh sách rỗng. Giá trị RETURNED phải giữ MỐI QUAN HỆ kiểu giống hệt input (hoạt động với mọi loại phần tử, không ép kiểu).",
            "tests": [
                {"name": "trả về phần tử đầu cho mọi loại", "hint": "items.length ? items[0] : fallback — không gì thêm."},
            ],
        },
        "i2-group-by": {
            "title": "Group-By theo key",
            "prompt": "Viết `groupBy(items, keyFn)` RETURN một object ánh xạ mỗi key sang mảng các item có key đó (thứ tự được giữ trong từng nhóm). Viết `keyCount(groups)` nhận kết quả đó và trả về số key khác nhau.",
            "tests": [
                {"name": "các nhóm giữ thứ tự item", "hint": "(acc[k] ??= []).push(item) khi duyệt mảng một lần."},
                {"name": "input rỗng cho nhóm rỗng", "hint": "Vòng lặp đơn giản là không chạy."},
            ],
        },
        "i2-result-wrap": {
            "title": "Wrapper kết quả",
            "prompt": "Viết `attempt(fn)` — gọi `fn` không đối số. Khi thành công RETURN `{ ok: true, value }`; khi throw RETURN `{ ok: false, error: err.message }`. Giá trị giữ nguyên hình dạng mà fn trả về (số, mảng, object — bất cứ gì), chứng minh wrapper không phụ thuộc hình dạng.",
            "tests": [
                {"name": "bọc thành công và thất bại cho mọi hình dạng", "hint": "try { return { ok: true, value: fn() }; } catch (err) { return { ok: false, error: err.message }; }"},
            ],
        },
    },
    [
        ["i2-first-or", "function firstOr(items, fallback) {\n  return items.length > 0 ? items[0] : fallback;\n}", "function firstOr(items, fallback) {\n  return items[items.length] ?? fallback;\n}"],
        ["i2-group-by", "function groupBy(items, keyFn) {\n  const out = {};\n  for (const item of items) {\n    const k = keyFn(item);\n    (out[k] ??= []).push(item);\n  }\n  return out;\n}\nfunction keyCount(groups) {\n  return Object.keys(groups).length;\n}", "function groupBy(items, keyFn) {\n  return {};\n}\nfunction keyCount(groups) {\n  return 0;\n}"],
        ["i2-result-wrap", "function attempt(fn) {\n  try {\n    return { ok: true, value: fn() };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}", "function attempt(fn) {\n  return { ok: true, value: fn() };\n}"],
    ],
)

# ── boundaries-practice ─────────────────────────────────────────────────────
write_practice(
    MOD, "boundaries-practice",
    "Boundaries — Practice",
    "Defensive edges: unknown-payload validators, a localStorage round-trip guard, and safe JSON with parseWith.",
    "Biên Giới — Luyện tập",
    "Rìa phòng thủ: validator cho payload unknown, guard vòng lặp localStorage, và JSON an toàn với parseWith.",
    "unknown-never", 18, "intermediate",
    [
        {
            "id": "i2-unknown-handler",
            "title": "Unknown Payload Handler",
            "prompt": "Write `handleUnknown(payload)` that narrows honestly: arrays of strings → `{ kind: \"tags\", tags }` (trimmed); finite numbers → `{ kind: \"count\", count }`; objects with string `id` → `{ kind: \"entity\", id }`; anything else → `{ kind: \"reject\" }`. Never throw.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function handleUnknown(payload) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "each variant narrows correctly",
                    "code": fn_wrap("handleUnknown", "handleUnknown") + "\nconst t = handleUnknown([\" a \", \"b\"]);\nif (t.kind !== \"tags\" || t.tags.join() !== \"a,b\") throw new Error(\"String arrays → tags (trimmed).\");\nconst c = handleUnknown(42);\nif (c.kind !== \"count\" || c.count !== 42) throw new Error(\"Finite numbers → count.\");\nconst e = handleUnknown({ id: \"x1\", junk: true });\nif (e.kind !== \"entity\" || e.id !== \"x1\") throw new Error(\"Objects with string id → entity (extra fields ok).\");\nconst r = handleUnknown(Symbol ? \"just a string\" : 0);\nif (r.kind !== \"reject\") throw new Error(\"Bare strings do not match any variant.\");",
                    "hint": "Array.isArray first, then typeof, then the object check with an id field.",
                },
                {
                    "name": "never throws on junk",
                    "code": fn_wrap("handleUnknown", "handleUnknown") + "\nfor (const junk of [null, undefined, NaN, {}, () => 1]) {\n  let threw = false;\n  try { handleUnknown(junk); } catch { threw = true; }\n  if (threw) throw new Error(\"Junk input must produce a result object, not a throw (failed on: \" + String(junk) + \").\");\n}",
                    "hint": "Every branch guards its assumptions; the final fallback returns reject.",
                },
            ],
        },
        {
            "id": "i2-storage-guard",
            "title": "Storage Guard",
            "prompt": "Write `loadSetting(storage, key, fallback)` — `storage` provides `getItem`/`setItem`. Parse the stored JSON safely: missing key, invalid JSON, or wrong-typed value all RETURN `fallback`; only a value passing `isShape` (provided as an argument: `(v) => boolean`) returns `{ ok: true, value }`. Also write `saveSetting(storage, key, value)` that stores `JSON.stringify(value)`.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function loadSetting(storage, key, isShape, fallback) {\n  // your code\n}\n\nfunction saveSetting(storage, key, value) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "round-trip through a fake storage",
                    "code": fn_wrap("loadSetting, saveSetting", "loadSetting, saveSetting") + "\nconst m = new Map();\nconst storage = { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, v) };\nconst isStr = (v) => typeof v === \"string\";\nsaveSetting(storage, \"theme\", \"dark\");\nconst out = loadSetting(storage, \"theme\", isStr, \"light\");\nif (out.ok !== true || out.value !== \"dark\") throw new Error(\"Valid stored value round-trips.\");",
                    "hint": "JSON.parse inside try/catch; then isShape(parsed) decides ok vs fallback.",
                },
                {
                    "name": "corrupt or wrong-typed data falls back",
                    "code": fn_wrap("loadSetting, saveSetting", "loadSetting, saveSetting") + "\nconst m = new Map();\nconst storage = { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, v) };\nconst isNum = (v) => typeof v === \"number\" && Number.isFinite(v);\nm.set(\"bad\", \"{nope\");           // invalid JSON\nm.set(\"wrong\", JSON.stringify(\"42\")); // string, not number\nif (loadSetting(storage, \"missing\", isNum, 0).ok !== false) throw new Error(\"Missing keys fall back.\");\nif (loadSetting(storage, \"bad\", isNum, 0).ok !== false) throw new Error(\"Invalid JSON falls back.\");\nif (loadSetting(storage, \"wrong\", isNum, 0).ok !== false) throw new Error(\"Wrong-typed values fall back.\");",
                    "hint": "Three failure paths, one return: { ok: false, fallback }.",
                },
            ],
        },
        {
            "id": "i2-safe-json",
            "title": "Safe JSON Layer",
            "prompt": "Write `parseOr(raw, fallback)` — parse `raw` as JSON, RETURN the value or `fallback` on any failure (never throws; handles non-string inputs). Write `serialize(value, fallback)` — RETURN the JSON string of `value`, or `fallback` when the value cannot be serialized (circular references, BigInt).",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function parseOr(raw, fallback) {\n  // your code\n}\n\nfunction serialize(value, fallback) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "parseOr is total",
                    "code": fn_wrap("parseOr, serialize", "parseOr, serialize") + "\nif (parseOr(\"[1,2]\", null).length !== 2) throw new Error(\"Valid JSON parses.\");\nif (parseOr(\"{oops\", \"fb\") !== \"fb\") throw new Error(\"Invalid JSON yields the fallback.\");\nif (parseOr(undefined, \"fb\") !== \"fb\") throw new Error(\"Non-string input yields the fallback.\");",
                    "hint": "try/catch around JSON.parse covers non-strings too.",
                },
                {
                    "name": "serialize survives circular references",
                    "code": fn_wrap("parseOr, serialize", "parseOr, serialize") + "\nif (serialize({ a: 1 }, \"fb\") === \"fb\" || serialize({ a: 1 }, \"fb\") === undefined) throw new Error(\"Plain objects serialize.\");\nconst circular = {};\ncircular.self = circular;\nif (serialize(circular, \"fb\") !== \"fb\") throw new Error(\"Circular structures return the fallback instead of throwing.\");",
                    "hint": "JSON.stringify throws on cycles — wrap it and return fallback in the catch.",
                },
            ],
        },
    ],
    {
        "i2-unknown-handler": {
            "title": "Bộ xử lý payload unknown",
            "prompt": "Viết `handleUnknown(payload)` thu hẹp kiểu một cách trung thực: mảng chuỗi → `{ kind: \"tags\", tags }` (đã trim); số hữu hạn → `{ kind: \"count\", count }`; object có `id` là chuỗi → `{ kind: \"entity\", id }`; mọi thứ khác → `{ kind: \"reject\" }`. Không bao giờ throw.",
            "tests": [
                {"name": "mỗi biến thể thu hẹp đúng", "hint": "Array.isArray trước, rồi typeof, rồi kiểm tra object với trường id."},
                {"name": "không bao giờ throw với rác", "hint": "Mỗi nhánh tự chặn giả định của mình; fallback cuối trả về reject."},
            ],
        },
        "i2-storage-guard": {
            "title": "Guard cho storage",
            "prompt": "Viết `loadSetting(storage, key, isShape, fallback)` — `storage` cung cấp `getItem`/`setItem`. Parse JSON đã lưu một cách an toàn: key không có, JSON không hợp lệ, hoặc giá trị sai kiểu đều RETURN `fallback`; chỉ giá trị vượt qua `isShape` (được truyền vào: `(v) => boolean`) mới trả về `{ ok: true, value }`. Đồng thời viết `saveSetting(storage, key, value)` lưu `JSON.stringify(value)`.",
            "tests": [
                {"name": "vòng lặp qua storage giả", "hint": "JSON.parse trong try/catch; rồi isShape(parsed) quyết định ok hay fallback."},
                {"name": "dữ liệu hỏng hoặc sai kiểu rơi về fallback", "hint": "Ba đường thất bại, một return: { ok: false, fallback }."},
            ],
        },
        "i2-safe-json": {
            "title": "Tầng JSON an toàn",
            "prompt": "Viết `parseOr(raw, fallback)` — parse `raw` thành JSON, RETURN giá trị hoặc `fallback` khi có bất kỳ lỗi nào (không bao giờ throw; xử lý cả input không phải chuỗi). Viết `serialize(value, fallback)` — RETURN chuỗi JSON của `value`, hoặc `fallback` khi giá trị không thể serialize (tham chiếu vòng, BigInt).",
            "tests": [
                {"name": "parseOr là hàm toàn phần", "hint": "try/catch quanh JSON.parse phủ luôn cả input không phải chuỗi."},
                {"name": "serialize sống sót qua tham chiếu vòng", "hint": "JSON.stringify throw với chu kỳ — bọc lại và trả fallback trong catch."},
            ],
        },
    },
    [
        ["i2-unknown-handler", "function handleUnknown(payload) {\n  if (Array.isArray(payload) && payload.every((x) => typeof x === \"string\")) {\n    return { kind: \"tags\", tags: payload.map((s) => s.trim()) };\n  }\n  if (typeof payload === \"number\" && Number.isFinite(payload)) {\n    return { kind: \"count\", count: payload };\n  }\n  if (payload && typeof payload === \"object\" && typeof payload.id === \"string\") {\n    return { kind: \"entity\", id: payload.id };\n  }\n  return { kind: \"reject\" };\n}", "function handleUnknown(payload) {\n  return { kind: \"tags\", tags: payload };\n}"],
        ["i2-storage-guard", "function loadSetting(storage, key, isShape, fallback) {\n  let parsed;\n  try {\n    const raw = storage.getItem(key);\n    if (raw === null) return { ok: false, fallback };\n    parsed = JSON.parse(raw);\n  } catch {\n    return { ok: false, fallback };\n  }\n  if (!isShape(parsed)) return { ok: false, fallback };\n  return { ok: true, value: parsed };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, JSON.stringify(value));\n}", "function loadSetting(storage, key, isShape, fallback) {\n  return { ok: true, value: JSON.parse(storage.getItem(key)) };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, value);\n}"],
        ["i2-safe-json", "function parseOr(raw, fallback) {\n  try {\n    return JSON.parse(raw);\n  } catch {\n    return fallback;\n  }\n}\nfunction serialize(value, fallback) {\n  try {\n    return JSON.stringify(value);\n  } catch {\n    return fallback;\n  }\n}", "function parseOr(raw, fallback) {\n  return JSON.parse(raw);\n}\nfunction serialize(value, fallback) {\n  return JSON.stringify(value);\n}"],
    ],
)

# ── ts-client-practice (mini build) ─────────────────────────────────────────
write_practice(
    MOD, "ts-client-practice",
    "Mini Build: Typed API Model",
    "Model a real API end-to-end at runtime: DTO validators, a discriminated result shape, and a typed-feel client wrapper.",
    "Dự án nhỏ: Mô hình API có kiểu",
    "Mô hình hóa một API thật trọn vẹn ở tầng runtime: validator DTO, hình dạng kết quả discriminated, và wrapper client mang cảm giác kiểu.",
    "type-safe-checkpoint", 22, "intermediate",
    [
        {
            "id": "i2-dto-validators",
            "title": "DTO Validators",
            "prompt": "Write `isTaskDTO(v)` — true only for objects with string `id`, non-empty string `title`, boolean `done`, and optional string `due` (absent or string). Write `isTaskListDTO(v)` — true only for arrays where every element passes `isTaskDTO`.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function isTaskDTO(v) {\n  // your code\n}\n\nfunction isTaskListDTO(v) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "accepts valid DTOs, with and without due",
                    "code": fn_wrap("isTaskDTO, isTaskListDTO", "isTaskDTO, isTaskListDTO") + "\nif (isTaskDTO({ id: \"t1\", title: \"ship\", done: false }) !== true) throw new Error(\"Minimal DTO accepted.\");\nif (isTaskDTO({ id: \"t1\", title: \"ship\", done: true, due: \"2026-10-01\" }) !== true) throw new Error(\"Optional due accepted.\");\nif (isTaskDTO({ id: \"t1\", title: \"\", done: false }) !== false) throw new Error(\"Empty title fails (non-empty required).\");\nif (isTaskListDTO([]) !== true) throw new Error(\"An empty list is a valid list.\");\nif (isTaskListDTO([{ id: \"t1\", title: \"ship\", done: false }, null]) !== false) throw new Error(\"One bad element fails the whole list.\");",
                    "hint": "title.trim().length > 0 for non-empty; Array.isArray + every for the list.",
                },
            ],
        },
        {
            "id": "i2-api-result",
            "title": "Discriminated API Result",
            "prompt": "Write `toApiResult(promise)` — awaits the promise and returns `{ ok: true, data }` on success, `{ ok: false, status: 0, message: err.message }` on failure. Write `unwrap(result)` — returns `data` when ok, else THROWS an Error with the stored message. The pair must compose: `unwrap(toApiResult(p))` returns the value or throws.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function toApiResult(promise) {\n  // your code\n}\n\nfunction unwrap(result) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "success and failure shapes",
                    "code": fn_wrap("toApiResult, unwrap", "toApiResult, unwrap") + "\nconst ok = await toApiResult(Promise.resolve({ n: 1 }));\nif (ok.ok !== true || ok.data.n !== 1) throw new Error(\"Success: { ok: true, data }.\");\nconst bad = await toApiResult(Promise.reject(new Error(\"boom\")));\nif (bad.ok !== false || bad.status !== 0 || bad.message !== \"boom\") throw new Error(\"Failure: { ok: false, status: 0, message }.\");",
                    "hint": "await inside try/catch; catch returns the failure object.",
                },
                {
                    "name": "unwrap composes with toApiResult",
                    "code": fn_wrap("toApiResult, unwrap", "toApiResult, unwrap") + "\nconst v = unwrap(await toApiResult(Promise.resolve(42)));\nif (v !== 42) throw new Error(\"unwrap returns the data on success.\");\nlet err;\ntry { unwrap(await toApiResult(Promise.reject(new Error(\"gone\")))); } catch (e) { err = e; }\nif (!err || err.message !== \"gone\") throw new Error(\"unwrap rethrows with the stored message.\");",
                    "hint": "result.ok ? result.data : (() => { throw new Error(result.message); })()",
                },
            ],
        },
        {
            "id": "i2-typed-client",
            "title": "Typed-Feel Client",
            "prompt": "Write `createTypedClient(fetchImpl)` where every method validates BEFORE returning:\n\n- `getTask(id)` — fetches `/tasks/{id}`; if the body passes `isTaskDTO` return `{ ok: true, task }`; a 404 returns `{ ok: false, reason: \"not-found\" }`; a malformed body returns `{ ok: false, reason: \"invalid\" }`\n- `listTasks()` — fetches `/tasks`; valid list → `{ ok: true, tasks }`; malformed → `{ ok: false, reason: \"invalid\" }`\n- the fake `fetchImpl(url)` returns `{ ok, status, json: async () => body }`",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function createTypedClient(fetchImpl) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "valid task flows through",
                    "code": fn_wrap("createTypedClient", "createTypedClient") + "\nconst task = { id: \"t1\", title: \"ship\", done: false };\nconst c = createTypedClient(async (u) => ({ ok: true, status: 200, json: async () => task }));\nconst out = await c.getTask(\"t1\");\nif (out.ok !== true || out.task.title !== \"ship\") throw new Error(\"A valid DTO returns { ok: true, task }.\");",
                    "hint": "Fetch, parse, then isTaskDTO(body) decides the shape of your result.",
                },
                {
                    "name": "not-found and invalid are distinct failures",
                    "code": fn_wrap("createTypedClient", "createTypedClient") + "\nconst c404 = createTypedClient(async () => ({ ok: false, status: 404, json: async () => ({}) }));\nif ((await c404.getTask(\"x\")).reason !== \"not-found\") throw new Error(\"A 404 maps to reason 'not-found'.\");\nconst cBad = createTypedClient(async () => ({ ok: true, status: 200, json: async () => ({ junk: true }) }));\nif ((await cBad.getTask(\"x\")).reason !== \"invalid\") throw new Error(\"A malformed body maps to reason 'invalid'.\");\nconst cBadList = createTypedClient(async () => ({ ok: true, status: 200, json: async () => ({ not: \"a list\" }) }));\nif ((await cBadList.listTasks()).reason !== \"invalid\") throw new Error(\"listTasks validates the whole list.\");",
                    "hint": "Check res.ok/res.status first (not-found), then validate the parsed body (invalid).",
                },
            ],
        },
    ],
    {
        "i2-dto-validators": {
            "title": "Validator DTO",
            "prompt": "Viết `isTaskDTO(v)` — true chỉ với object có `id` là chuỗi, `title` là chuỗi khác rỗng, `done` là boolean, và `due` tùy chọn (vắng mặt hoặc là chuỗi). Viết `isTaskListDTO(v)` — true chỉ với mảng mà mọi phần tử vượt qua `isTaskDTO`.",
            "tests": [
                {"name": "chấp nhận DTO hợp lệ, có hoặc không có due", "hint": "title.trim().length > 0 cho khác rỗng; Array.isArray + every cho danh sách."},
            ],
        },
        "i2-api-result": {
            "title": "Kết quả API dạng discriminated",
            "prompt": "Viết `toApiResult(promise)` — await promise và trả về `{ ok: true, data }` khi thành công, `{ ok: false, status: 0, message: err.message }` khi thất bại. Viết `unwrap(result)` — trả về `data` khi ok, nếu không THROW một Error với message đã lưu. Cặp hàm phải ghép được: `unwrap(toApiResult(p))` trả về giá trị hoặc throw.",
            "tests": [
                {"name": "hình dạng thành công và thất bại", "hint": "await bên trong try/catch; catch trả về object thất bại."},
                {"name": "unwrap ghép được với toApiResult", "hint": "result.ok ? result.data : (() => { throw new Error(result.message); })()"},
            ],
        },
        "i2-typed-client": {
            "title": "Client mang cảm giác kiểu",
            "prompt": "Viết `createTypedClient(fetchImpl)` trong đó mọi phương thức đều KIỂM TRA trước khi trả về:\n\n- `getTask(id)` — fetch `/tasks/{id}`; nếu body vượt qua `isTaskDTO` trả `{ ok: true, task }`; 404 trả `{ ok: false, reason: \"not-found\" }`; body dị dạng trả `{ ok: false, reason: \"invalid\" }`\n- `listTasks()` — fetch `/tasks`; danh sách hợp lệ → `{ ok: true, tasks }`; dị dạng → `{ ok: false, reason: \"invalid\" }`\n- `fetchImpl(url)` giả trả `{ ok, status, json: async () => body }`",
            "tests": [
                {"name": "task hợp lệ đi qua trọn vẹn", "hint": "Fetch, parse, rồi isTaskDTO(body) quyết định hình dạng kết quả của bạn."},
                {"name": "not-found và invalid là hai thất bại khác nhau", "hint": "Kiểm tra res.ok/res.status trước (not-found), rồi validate body đã parse (invalid)."},
            ],
        },
    },
    [
        ["i2-dto-validators", "function isTaskDTO(v) {\n  if (!v || typeof v !== \"object\" || Array.isArray(v)) return false;\n  if (typeof v.id !== \"string\") return false;\n  if (typeof v.title !== \"string\" || v.title.trim().length === 0) return false;\n  if (typeof v.done !== \"boolean\") return false;\n  if (v.due !== undefined && typeof v.due !== \"string\") return false;\n  return true;\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}", "function isTaskDTO(v) { return !!v; }\nfunction isTaskListDTO(v) { return Array.isArray(v); }"],
        ["i2-api-result", "async function toApiResult(promise) {\n  try {\n    const data = await promise;\n    return { ok: true, data };\n  } catch (err) {\n    return { ok: false, status: 0, message: err.message };\n  }\n}\nfunction unwrap(result) {\n  if (result.ok) return result.data;\n  throw new Error(result.message);\n}", "async function toApiResult(promise) {\n  const data = await promise;\n  return { ok: true, data };\n}\nfunction unwrap(result) {\n  return result.data;\n}"],
        ["i2-typed-client", "function createTypedClient(fetchImpl) {\n  async function getJSON(url) {\n    const res = await fetchImpl(url);\n    return { res, body: await res.json() };\n  }\n  return {\n    async getTask(id) {\n      const { res, body } = await getJSON(\"/tasks/\" + id);\n      if (!res.ok) return { ok: false, reason: \"not-found\" };\n      if (!isTaskDTO(body)) return { ok: false, reason: \"invalid\" };\n      return { ok: true, task: body };\n    },\n    async listTasks() {\n      const { res, body } = await getJSON(\"/tasks\");\n      if (!res.ok || !isTaskListDTO(body)) return { ok: false, reason: \"invalid\" };\n      return { ok: true, tasks: body };\n    },\n  };\n}\nfunction isTaskDTO(v) {\n  if (!v || typeof v !== \"object\" || Array.isArray(v)) return false;\n  return typeof v.id === \"string\" && typeof v.title === \"string\" && v.title.length > 0 && typeof v.done === \"boolean\";\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}", "function createTypedClient(fetchImpl) {\n  return {\n    async getTask(id) {\n      const res = await fetchImpl(\"/tasks/\" + id);\n      return { ok: true, task: await res.json() };\n    },\n    async listTasks() {\n      const res = await fetchImpl(\"/tasks\");\n      return { ok: true, tasks: await res.json() };\n    },\n  };\n}"],
    ],
)

print("Module 5 practices written.")
