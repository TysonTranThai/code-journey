/**
 * Module 1 completion: error-handling + data-explorer-checkpoint lessons,
 * destructuring/error-handling/data-explorer practice sets, module manifest
 * with VI overlay. Run after i2-m1.mjs. Idempotent.
 */
import { T, writeModule, writeLesson, writeCheckpoint, writePracticeSet } from "./i2-lib.mjs";

const MOD = "modern-javascript";

writeModule(MOD, {
  title: "Modern JavaScript",
  summary:
    "The professional JavaScript layer: closures and modules, higher-order functions, Map/Set, destructuring, and error handling — applied through data transformation.",
  viTitle: "Modern JavaScript",
  viSummary:
    "Tầng JavaScript chuyên nghiệp: closure và module, hàm bậc cao, Map/Set, destructuring và xử lý lỗi — vận dụng qua các bài toán biến đổi dữ liệu.",
  lessons: [
    "scope-closures",
    "higher-order-functions",
    "destructuring-spread",
    "modules-import-export",
    "map-set-structured-data",
    "error-handling",
    "data-explorer-checkpoint",
  ],
  practices: [
    "closures-practice",
    "hof-practice",
    "modules-practice",
    "destructuring-practice",
    "map-set-practice",
    "error-handling-practice",
    "data-explorer-practice",
  ],
});

// ── Lesson: error-handling ──────────────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "error-handling",
    title: "Deliberate Error Handling",
    description:
      "Expected vs unexpected failures, custom error classes, targeted try/catch, and the result-object pattern — an error strategy for real programs.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
You already know an uncaught error crashes a program. What separates
intermediate code from beginner code is a **deliberate error strategy**: which
errors you expect, which you let crash, and how a failure travels between the
layers of a program.

## Expected vs unexpected errors

An **expected** error is part of the problem domain: a form field is empty, a
JSON string is malformed, a record does not exist. An **unexpected** error is a
bug: a typo, a missing function, an impossible state. You *handle* expected
errors and you *fix* unexpected ones. Wrapping your whole program in try/catch
hides bugs — the worst outcome.

## The shape of an Error

${T}throw${T} accepts any value, but always throw ${T}Error${T} instances — they
carry a ${T}message${T}, a ${T}stack${T} (dev-only detail), and since ES2022 a
${T}cause${T} for chaining:

~~~js
try {
  loadConfig(path);
} catch (err) {
  throw new Error("Config failed to load", { cause: err });
}
~~~

The built-in types have meaning: ${T}TypeError${T} for wrong types,
${T}RangeError${T} for out-of-range values, ${T}SyntaxError${T} from
${T}JSON.parse${T}. Reach for them before inventing your own.

## Custom errors

When callers need to *react* differently to a failure, give it a name:

~~~js
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

throw new ValidationError("age must be non-negative", "age");
~~~

Callers can now distinguish it with ${T}err instanceof ValidationError${T} —
string-matching messages is how bugs hide.

## Catch deliberately, narrowly

Catch only what you can actually handle, and rethrow the rest:

~~~js
try {
  const user = parseUser(raw);
  save(user);
} catch (err) {
  if (err instanceof ValidationError) {
    showFieldError(err.field, err.message); // ours: show a message
  } else {
    throw err; // not ours: let it propagate
  }
}
~~~

The optional ${T}finally${T} block runs whether or not an error occurred — use
it to release resources, not to return values.

## The result-object pattern

Across module boundaries, expected failures are often better as **values** than
thrown exceptions. Return ${T}{ ok: true, value }${T} or
${T}{ ok: false, error }${T} and force the caller to acknowledge the failure —
this is how the parser practice below is shaped. Rule of thumb: throw for
programmer-visible failures, return results for ordinary, expected ones.
`,
  },
  {
    title: "Xử lý lỗi có chủ đích",
    description:
      "Lỗi dự liệu được và lỗi bất ngờ, class lỗi tùy biến, try/catch có chọn lọc và mẫu result object — chiến lược xử lý lỗi cho chương trình thực thụ.",
    mdx: `
Bạn đã biết lỗi không được bắt sẽ làm chương trình đổ vỡ. Điều phân biệt code
trung cấp với code người mới bắt đầu là **chiến lược xử lý lỗi có chủ đích**:
lỗi nào bạn dự liệu được, lỗi nào để mặc nó đổ vỡ, và một lỗi di chuyển giữa
các tầng của chương trình như thế nào.

## Lỗi dự liệu được và lỗi bất ngờ

**Lỗi dự liệu được** là một phần của bài toán: trường biểu mẫu bị bỏ trống,
chuỗi JSON sai định dạng, bản ghi không tồn tại. **Lỗi bất ngờ** là bug: gõ sai
tên, gọi function không tồn tại, một trạng thái không thể xảy ra. Bạn *xử lý*
lỗi dự liệu được và *sửa* lỗi bất ngờ. Bọc cả chương trình trong try/catch chỉ
giấuđi bug — điều tệ nhất có thể làm.

## Cấu trúc của một Error

${T}throw${T} nhận bất kỳ giá trị nào, nhưng hãy luôn throw instance của
${T}Error${T} — nó mang theo ${T}message${T}, ${T}stack${T} (chi tiết chỉ dành
cho dev) và từ ES2022 có thêm ${T}cause${T} để nối chuỗi lỗi:

~~~js
try {
  loadConfig(path);
} catch (err) {
  throw new Error("Config failed to load", { cause: err });
}
~~~

Các loại lỗi có sẵn đều có ý nghĩa: ${T}TypeError${T} cho sai kiểu,
${T}RangeError${T} cho giá trị ngoài khoảng, ${T}SyntaxError${T} từ
${T}JSON.parse${T}. Hãy dùng chúng trước khi tự chế loại lỗi riêng.

## Lỗi tùy biến

Khi caller cần *phản ứng* khác nhau với từng loại thất bại, hãy đặt cho nó một
cái tên:

~~~js
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

throw new ValidationError("age must be non-negative", "age");
~~~

Caller giờ đây có thể phân biệt bằng ${T}err instanceof ValidationError${T} —
so sánh chuỗi message chính là cách giấu bug.

## Bắt lỗi có chọn lọc

Chỉ bắt những lỗi bạn thực sự xử lý được, những lỗi còn lại hãy ném tiếp:

~~~js
try {
  const user = parseUser(raw);
  save(user);
} catch (err) {
  if (err instanceof ValidationError) {
    showFieldError(err.field, err.message); // lỗi của ta: hiện thông báo
  } else {
    throw err; // không phải của ta: để nó lan tiếp
  }
}
~~~

Khối ${T}finally${T} (tùy chọn) luôn chạy dù có lỗi hay không — dùng nó để dọn
dẹp tài nguyên, không dùng để return giá trị.

## Mẫu result object

Khi vượt qua ranh giới module, thất bại dự liệu được thường nên là **giá trị**
thay vì exception. Hãy return ${T}{ ok: true, value }${T} hoặc
${T}{ ok: false, error }${T} để buộc caller phải đối diện với thất bại — bài
luyện tập về parser phía dưới được thiết kế theo đúng mẫu này. Nguyên tắc chung:
throw cho những lỗi mà lập trình viên cần thấy, return result cho các thất bại
bình thường, dự liệu được.
`,
  },
);

// ── Lesson: data-explorer-checkpoint (checkpoint) ───────────────────────────
writeCheckpoint(
  MOD,
  {
    id: "data-explorer-checkpoint",
    title: "Checkpoint: Data Explorer Core",
    description:
      "Combine closures, higher-order functions, Map/Set, destructuring, and error handling into the core of a small data explorer.",
    minutes: 20,
    difficulty: "intermediate",
    mdx: `
Six lessons in, you now own the JavaScript layer real applications are written
in: closures for private state, higher-order functions for data flow, Map and
Set for indexed lookups, destructuring for clean extraction, and deliberate
error handling.

No new theory here. The challenge below asks you to combine all five into the
core of a small **data explorer** — grouping, deduplication, summarizing, and
safe access — the same shape of code the module project builds on.

Requirements:

1. ${T}groupBy(records, keyFn)${T} — returns a plain object mapping each key to
   the array of records with that key.
2. ${T}uniqueBy(records, keyFn)${T} — returns the records deduplicated by key,
   keeping the **first** occurrence of each.
3. ${T}summarize(records)${T} — returns ${T}{ count, avgScore, top }${T} where
   ${T}avgScore${T} is the mean of the ${T}score${T} fields and ${T}top${T} is
   the record with the highest score. An empty list yields
   ${T}{ count: 0, avgScore: 0, top: null }${T}.
4. ${T}safeGet(records, index)${T} — returns the record at ${T}index${T}, or
   ${T}null${T} for out-of-range or non-integer indexes. It must **never
   throw**.

Take your time — the tests check each function separately, so you can build and
verify them one at a time.
`,
  },
  {
    title: "Kiểm tra kiến thức: Lõi Trình khám phá dữ liệu",
    description:
      "Kết hợp closure, hàm bậc cao, Map/Set, destructuring và xử lý lỗi để xây phần lõi của một trình khám phá dữ liệu nhỏ.",
    mdx: `
Sau sáu bài học, bạn đã nắm được tầng JavaScript mà các ứng dụng thực thụ được
viết bằng: closure cho private state, hàm bậc cao cho luồng dữ liệu, Map và Set
cho tra cứu theo chỉ mục, destructuring để trích xuất gọn gàng, và xử lý lỗi có
chủ đích.

Không có lý thuyết mới ở đây. Thử thách bên dưới yêu cầu bạn kết hợp cả năm kỹ
thuật đó vào phần lõi của một **trình khám phá dữ liệu** nhỏ — gom nhóm, khử
trùng lặp, tổng hợp và truy cập an toàn — chính là hình dạng code mà dự án của
module này sẽ xây tiếp.

Yêu cầu:

1. ${T}groupBy(records, keyFn)${T} — trả về một object thường, ánh xạ mỗi key
   sang mảng các bản ghi có key đó.
2. ${T}uniqueBy(records, keyFn)${T} — trả về các bản ghi đã khử trùng lặp theo
   key, giữ lại lần xuất hiện **đầu tiên** của mỗi key.
3. ${T}summarize(records)${T} — trả về ${T}{ count, avgScore, top }${T} trong
   đó ${T}avgScore${T} là trung bình cộng của trường ${T}score${T} còn
   ${T}top${T} là bản ghi có điểm cao nhất. Danh sách rỗng cho kết quả
   ${T}{ count: 0, avgScore: 0, top: null }${T}.
4. ${T}safeGet(records, index)${T} — trả về bản ghi tại vị trí ${T}index${T},
   hoặc ${T}null${T} nếu index vượt phạm vi hoặc không phải số nguyên. Hàm này
   **không được phép throw**.

Cứ từ từ — các test kiểm tra từng function riêng biệt, nên bạn có thể xây và
kiểm chứng từng cái một.
`,
  },
  {
    id: "i2-data-explorer-checkpoint",
    title: "Data Explorer Core Check",
    prompt:
      "Build the core of a data explorer:\n\n1. `groupBy(records, keyFn)` RETURNS a plain object mapping each key (from `keyFn(record)`) to the array of matching records.\n2. `uniqueBy(records, keyFn)` RETURNS the records deduplicated by key, keeping the first occurrence of each.\n3. `summarize(records)` RETURNS `{ count, avgScore, top }` — the record count, the mean of the `score` fields, and the whole record with the highest score. Empty input returns `{ count: 0, avgScore: 0, top: null }`.\n4. `safeGet(records, index)` RETURNS the record at `index`, or `null` when the index is out of range or not an integer. It must never throw.",
    difficulty: "intermediate",
    boilerplate:
      "// Build the core of a data explorer.\n\n// 1) groupBy(records, keyFn)\n\n// 2) uniqueBy(records, keyFn)\n\n// 3) summarize(records)\n\n// 4) safeGet(records, index)\n",
    tests: [
      {
        name: "groupBy groups records by keyFn",
        code: 'const fn = new Function(code + "\\nreturn { groupBy, uniqueBy, summarize, safeGet };");\nconst { groupBy } = fn();\nconst recs = [\n  { id: 1, kind: "fruit", score: 2 },\n  { id: 2, kind: "veg", score: 5 },\n  { id: 3, kind: "fruit", score: 9 },\n];\nconst out = groupBy(recs, (r) => r.kind);\nif (out.fruit.length !== 2 || out.veg.length !== 1) throw new Error("groupBy should bucket records by the keyFn result.");\nif (out.fruit[0].id !== 1 || out.fruit[1].id !== 3) throw new Error("groupBy must preserve record order within each bucket.");',
        hint: "Walk the array once; for each key, push into (out[key] ??= []).",
      },
      {
        name: "uniqueBy keeps the first occurrence per key",
        code: 'const fn = new Function(code + "\\nreturn { groupBy, uniqueBy, summarize, safeGet };");\nconst { uniqueBy } = fn();\nconst recs = [\n  { id: 1, kind: "fruit" },\n  { id: 2, kind: "veg" },\n  { id: 3, kind: "fruit" },\n];\nconst out = uniqueBy(recs, (r) => r.kind);\nif (out.length !== 2 || out[0].id !== 1 || out[1].id !== 2) throw new Error("uniqueBy should keep only the FIRST record per key, in order.");',
        hint: "Track seen keys in a Set; push the record only when the key is new.",
      },
      {
        name: "summarize computes count, average, and top",
        code: 'const fn = new Function(code + "\\nreturn { groupBy, uniqueBy, summarize, safeGet };");\nconst { summarize } = fn();\nconst recs = [{ score: 4 }, { score: 8 }, { score: 6 }];\nconst s = summarize(recs);\nif (s.count !== 3) throw new Error("count should be the number of records.");\nif (Math.abs(s.avgScore - 6) > 1e-9) throw new Error("avgScore should be the mean of the score fields (6 here).");\nif (!s.top || s.top.score !== 8) throw new Error("top should be the WHOLE record with the highest score.");\nconst empty = summarize([]);\nif (empty.count !== 0 || empty.avgScore !== 0 || empty.top !== null) throw new Error("Empty input must yield { count: 0, avgScore: 0, top: null }.");',
        hint: "Guard the empty case first; then loop once accumulating sum and best-so-far.",
      },
      {
        name: "safeGet never throws and returns null for bad indexes",
        code: 'const fn = new Function(code + "\\nreturn { groupBy, uniqueBy, summarize, safeGet };");\nconst { safeGet } = fn();\nconst recs = [{ id: 1 }, { id: 2 }];\nif (safeGet(recs, 0)?.id !== 1) throw new Error("safeGet(recs, 0) should return the first record.");\nif (safeGet(recs, 5) !== null) throw new Error("Out-of-range index must return null, not throw.");\nif (safeGet(recs, 1.5) !== null) throw new Error("Non-integer index must return null.");\nif (safeGet(recs, -1) !== null) throw new Error("Negative index must return null.");',
        hint: "Check Number.isInteger(index) and 0 <= index < records.length before touching the array.",
      },
    ],
  },
  {
    title: "Kiểm tra kiến thức: Lõi Trình khám phá dữ liệu",
    prompt:
      "Xây phần lõi của một trình khám phá dữ liệu:\n\n1. `groupBy(records, keyFn)` RETURN một object thường, ánh xạ mỗi key (từ `keyFn(record)`) sang mảng các bản ghi khớp với key đó.\n2. `uniqueBy(records, keyFn)` RETURN các bản ghi đã khử trùng lặp theo key, giữ lại lần xuất hiện đầu tiên của mỗi key.\n3. `summarize(records)` RETURN `{ count, avgScore, top }` — số bản ghi, trung bình cộng của các trường `score`, và toàn bộ bản ghi có điểm cao nhất. Input rỗng trả về `{ count: 0, avgScore: 0, top: null }`.\n4. `safeGet(records, index)` RETURN bản ghi tại vị trí `index`, hoặc `null` khi index vượt phạm vi hoặc không phải số nguyên. Hàm không được phép throw.",
    tests: [
      {
        name: "groupBy gom nhóm bản ghi theo keyFn",
        hint: "Duyệt mảng một lần; với mỗi key, push vào (out[key] ??= []).",
      },
      {
        name: "uniqueBy giữ lần xuất hiện đầu tiên theo key",
        hint: "Dùng Set theo dõi các key đã gặp; chỉ push bản ghi khi key là mới.",
      },
      {
        name: "summarize tính count, trung bình và top",
        hint: "Xử lý trường hợp rỗng trước; sau đó duyệt một vòng, cùng lúc cộng dồn tổng và ghi nhớ bản ghi tốt nhất.",
      },
      {
        name: "safeGet không bao giờ throw, trả null cho index xấu",
        hint: "Kiểm tra Number.isInteger(index) và 0 <= index < records.length trước khi đụng vào mảng.",
      },
    ],
  },
);

// ── Practice: destructuring-practice ────────────────────────────────────────
writePracticeSet(
  MOD,
  {
    file: "destructuring-practice.json",
    id: "destructuring-practice",
    title: "Destructuring & Spread — Practice",
    description:
      "Extract and combine data with destructuring, rest, and spread: pick fields, merge settings, and summarize with rest parameters.",
    viTitle: "Destructuring & Spread — Luyện tập",
    viDescription:
      "Trích xuất và kết hợp dữ liệu bằng destructuring, rest và spread: chọn trường, gộp cấu hình và thống kê với tham số rest.",
    afterLesson: "destructuring-spread",
    minutes: 15,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-pick-fields",
        title: "Pick Fields",
        prompt:
          "Write `pick(obj, keys)` that RETURNS a new object containing only the properties listed in `keys` that actually exist on `obj`. Missing keys are skipped, the input object must never be mutated, and each call returns a fresh object.",
        difficulty: "intermediate",
        level: "guided",
        boilerplate: "function pick(obj, keys) {\n  // your code\n}\n",
        tests: [
          {
            name: "picks only the listed keys",
            code: 'const fn = new Function(code + "\\nreturn { pick };");\nconst { pick } = fn();\nconst out = pick({ a: 1, b: 2, c: 3 }, ["a", "c"]);\nif (out.a !== 1 || out.c !== 3 || "b" in out) throw new Error("pick({ a: 1, b: 2, c: 3 }, [\\"a\\", \\"c\\"]) should be exactly { a: 1, c: 3 }.");',
            hint: "Start with an empty object and copy key by key — or destructure with rest and rebuild.",
          },
          {
            name: "skips missing keys",
            code: 'const fn = new Function(code + "\\nreturn { pick };");\nconst { pick } = fn();\nconst out = pick({ a: 1 }, ["a", "z"]);\nif (out.a !== 1 || "z" in out) throw new Error("Keys that do not exist on the object must be skipped, not added as undefined.");',
            hint: "Check `k in obj` before copying.",
          },
          {
            name: "returns a new object and does not mutate the input",
            code: 'const fn = new Function(code + "\\nreturn { pick };");\nconst { pick } = fn();\nconst input = { a: 1, b: 2 };\nconst out = pick(input, ["a"]);\nif (out === input) throw new Error("pick must return a NEW object, not the input.");\nif (input.b !== 2 || Object.keys(input).length !== 2) throw new Error("The input object must stay unchanged.");',
            hint: "Never write to obj — build the result separately.",
          },
        ],
        vi: {
          title: "Chọn trường với pick",
          prompt:
            "Viết `pick(obj, keys)` RETURN một object mới chỉ chứa các thuộc tính được liệt kê trong `keys` và thực sự tồn tại trên `obj`. Key không có sẽ bị bỏ qua, object input không bao giờ bị thay đổi, và mỗi lần gọi trả về một object mới.",
          tests: [
            {
              name: "chỉ chọn đúng các key được liệt kê",
              hint: "Bắt đầu từ object rỗng và copy từng key — hoặc dùng destructuring với rest rồi dựng lại.",
            },
            { name: "bỏ qua key không tồn tại", hint: "Kiểm tra `k in obj` trước khi copy." },
            {
              name: "trả về object mới, không làm thay đổi input",
              hint: "Đừng ghi vào obj — hãy dựng kết quả riêng.",
            },
          ],
        },
      },
      {
        id: "i2-merge-settings",
        title: "Merge Settings",
        prompt:
          "Write `mergeSettings(defaults, overrides)` that RETURNS a new object containing every key from `defaults` plus every key from `overrides`, with `overrides` values winning on conflicts. Neither input object may be mutated.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function mergeSettings(defaults, overrides) {\n  // your code\n}\n",
        tests: [
          {
            name: "overrides win on conflicts",
            code: 'const fn = new Function(code + "\\nreturn { mergeSettings };");\nconst { mergeSettings } = fn();\nconst out = mergeSettings({ a: 1, b: 2 }, { b: 9 });\nif (out.a !== 1 || out.b !== 9) throw new Error("mergeSettings({ a: 1, b: 2 }, { b: 9 }) should be { a: 1, b: 9 } — later sources win.");',
            hint: "Spread both objects into a new one, defaults first.",
          },
          {
            name: "extra override keys flow through",
            code: 'const fn = new Function(code + "\\nreturn { mergeSettings };");\nconst { mergeSettings } = fn();\nconst out = mergeSettings({ theme: "light" }, { fontSize: 14 });\nif (out.theme !== "light" || out.fontSize !== 14) throw new Error("Keys that only exist in overrides should still appear in the result.");',
            hint: "A single spread of each source handles both directions.",
          },
          {
            name: "neither input is mutated",
            code: 'const fn = new Function(code + "\\nreturn { mergeSettings };");\nconst { mergeSettings } = fn();\nconst d = { a: 1 };\nconst o = { a: 2, b: 3 };\nconst out = mergeSettings(d, o);\nif (d.a !== 1 || Object.keys(d).length !== 1) throw new Error("defaults must not be mutated — Object.assign(d, o) is the classic mistake.");\nif (o.a !== 2 || o.b !== 3) throw new Error("overrides must not be mutated.");\nif (out === d || out === o) throw new Error("The result must be a fresh object.");',
            hint: "Build a new object; never write into either argument.",
          },
        ],
        vi: {
          title: "Gộp cấu hình",
          prompt:
            "Viết `mergeSettings(defaults, overrides)` RETURN một object mới chứa mọi key từ `defaults` cộng với mọi key từ `overrides`, giá trị của `overrides` thắng khi xung đột. Không được làm thay đổi object input nào.",
          tests: [
            {
              name: "overrides thắng khi xung đột",
              hint: "Spread cả hai object vào một object mới, defaults trước.",
            },
            {
              name: "key chỉ có ở overrides vẫn được giữ",
              hint: "Một lần spread cho mỗi nguồn là xử lý được cả hai chiều.",
            },
            {
              name: "không thay đổi cả hai input",
              hint: "Dựng object mới; đừng bao giờ ghi vào tham số đầu vào. Object.assign(d, o) là lỗi kinh điển.",
            },
          ],
        },
      },
      {
        id: "i2-stats",
        title: "Rest-Parameter Statistics",
        prompt:
          "Write `stats(...numbers)` that accepts any number of numeric arguments and RETURNS `{ min, max, avg }`. Called with no arguments it RETURNS `{ min: 0, max: 0, avg: 0 }` instead of throwing.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function stats(...numbers) {\n  // your code\n}\n",
        tests: [
          {
            name: "finds min and max across many arguments",
            code: 'const fn = new Function(code + "\\nreturn { stats };");\nconst { stats } = fn();\nconst s = stats(3, 1, 4, 1, 5);\nif (s.min !== 1 || s.max !== 5) throw new Error("stats(3, 1, 4, 1, 5) should report min 1 and max 5.");',
            hint: "With rest parameters, numbers is a real array — loop it or use Math.min/Math.max with spread.",
          },
          {
            name: "avg is the mean",
            code: 'const fn = new Function(code + "\\nreturn { stats };");\nconst { stats } = fn();\nif (Math.abs(stats(2, 4, 6).avg - 4) > 1e-9) throw new Error("stats(2, 4, 6).avg should be 4.");\nif (Math.abs(stats(1, 2).avg - 1.5) > 1e-9) throw new Error("stats(1, 2).avg should be 1.5.");',
            hint: "Sum, then divide by numbers.length.",
          },
          {
            name: "empty call returns zeros without throwing",
            code: 'const fn = new Function(code + "\\nreturn { stats };");\nconst { stats } = fn();\nconst s = stats();\nif (s.min !== 0 || s.max !== 0 || s.avg !== 0) throw new Error("stats() with no arguments must return { min: 0, max: 0, avg: 0 }.");',
            hint: "Guard the empty case before reading numbers[0].",
          },
        ],
        vi: {
          title: "Thống kê với tham số rest",
          prompt:
            "Viết `stats(...numbers)` nhận bao nhiêu đối số số cũng được và RETURN `{ min, max, avg }`. Khi gọi không có đối số nào, RETURN `{ min: 0, max: 0, avg: 0 }` thay vì throw.",
          tests: [
            {
              name: "tìm min và max qua nhiều đối số",
              hint: "Với rest parameters, numbers là một mảng thật — duyệt nó hoặc dùng Math.min/Math.max với spread.",
            },
            { name: "avg là trung bình cộng", hint: "Cộng dồn rồi chia cho numbers.length." },
            {
              name: "gọi rỗng trả về số 0, không throw",
              hint: "Xử lý trường hợp rỗng trước khi đọc numbers[0].",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-pick-fields",
      "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}",
      "function pick(obj, keys) { return obj; }",
    ],
    [
      "i2-merge-settings",
      "function mergeSettings(defaults, overrides) {\n  return { ...defaults, ...overrides };\n}",
      "function mergeSettings(defaults, overrides) {\n  Object.assign(defaults, overrides);\n  return defaults;\n}",
    ],
    [
      "i2-stats",
      "function stats(...numbers) {\n  if (numbers.length === 0) return { min: 0, max: 0, avg: 0 };\n  let min = numbers[0], max = numbers[0], sum = 0;\n  for (const n of numbers) {\n    if (n < min) min = n;\n    if (n > max) max = n;\n    sum += n;\n  }\n  return { min, max, avg: sum / numbers.length };\n}",
      "function stats(...numbers) { return { min: numbers[0], max: numbers[0], avg: numbers[0] }; }",
    ],
  ],
);

// ── Practice: error-handling-practice ───────────────────────────────────────
writePracticeSet(
  MOD,
  {
    file: "error-handling-practice.json",
    id: "error-handling-practice",
    title: "Error Handling — Practice",
    description:
      "Catch safely, define custom errors, and retry failures: a safe JSON parser, a ValidationError class, and a retry helper.",
    viTitle: "Xử lý lỗi — Luyện tập",
    viDescription:
      "Bắt lỗi an toàn, định nghĩa lỗi tùy biến và thử lại khi thất bại: parser JSON an toàn, class ValidationError và hàm retry.",
    afterLesson: "error-handling",
    minutes: 18,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-safe-parse",
        title: "Safe JSON Parse",
        prompt:
          "Write `safeParse(json, fallback)` that RETURNS the parsed value when `json` is valid JSON, and RETURNS `fallback` when it is not. It must never throw, whatever the input.",
        difficulty: "intermediate",
        level: "guided",
        boilerplate: "function safeParse(json, fallback) {\n  // your code\n}\n",
        tests: [
          {
            name: "parses valid JSON",
            code: 'const fn = new Function(code + "\\nreturn { safeParse };");\nconst { safeParse } = fn();\nconst parsed = safeParse(\'{"a":1}\', null);\nif (!parsed || parsed.a !== 1) throw new Error("safeParse should parse that JSON text into an object whose a property is 1.");\nif (safeParse("[1,2]", null)?.length !== 2) throw new Error("safeParse should parse arrays too.");\nif (safeParse("42", 0) !== 42) throw new Error("A JSON number string parses to the number 42.");',
            hint: "JSON.parse handles objects, arrays, numbers, and strings — just wrap the call.",
          },
          {
            name: "returns the fallback for invalid JSON",
            code: 'const fn = new Function(code + "\\nreturn { safeParse };");\nconst { safeParse } = fn();\nif (safeParse("{nope", "x") !== "x") throw new Error("Invalid JSON must return the fallback, not throw.");\nif (safeParse("", null) !== null) throw new Error("An empty string is not valid JSON — return the fallback.");',
            hint: "try { return JSON.parse(json); } catch { return fallback; }",
          },
          {
            name: "never throws, whatever the input",
            code: 'const fn = new Function(code + "\\nreturn { safeParse };");\nconst { safeParse } = fn();\nfor (const bad of [undefined, null, {}, 123]) {\n  let threw = false;\n  try { safeParse(bad, "fb"); } catch { threw = true; }\n  if (threw) throw new Error("safeParse must not throw even when json is not a string at all (got: " + typeof bad + ").");\n}',
            hint: "The catch block catches JSON.parse's TypeError for non-string inputs too — no extra checks needed.",
          },
        ],
        vi: {
          title: "Parse JSON an toàn",
          prompt:
            "Viết `safeParse(json, fallback)` RETURN giá trị đã parse khi `json` là JSON hợp lệ, và RETURN `fallback` khi không phải. Hàm không bao giờ được throw, bất kể input là gì.",
          tests: [
            {
              name: "parse được JSON hợp lệ",
              hint: "JSON.parse xử lý được object, mảng, số và chuỗi — chỉ cần bọc lời gọi trong try.",
            },
            {
              name: "trả về fallback cho JSON không hợp lệ",
              hint: "try { return JSON.parse(json); } catch { return fallback; }",
            },
            {
              name: "không bao giờ throw, bất kể input",
              hint: "Khối catch cũng bắt được TypeError của JSON.parse khi input không phải chuỗi — không cần kiểm tra thêm.",
            },
          ],
        },
      },
      {
        id: "i2-validation-error",
        title: "Custom ValidationError",
        prompt:
          'Define `class ValidationError extends Error` with `name` set to `"ValidationError"`. Write `validateAge(age)` that THROWS a ValidationError with message `"age must be a number"` when `age` is not a number (or is NaN), and `"age must be non-negative"` when it is below 0. Write `tryValidateAge(age)` that RETURNS `{ ok: true, value: age }` on success and `{ ok: false, error }` when a ValidationError was thrown — any other error must still propagate.',
        difficulty: "intermediate",
        level: "independent",
        boilerplate:
          "class ValidationError extends Error {\n  // your code\n}\n\nfunction validateAge(age) {\n  // throws ValidationError\n}\n\nfunction tryValidateAge(age) {\n  // returns { ok, value? } or { ok: false, error }\n}\n",
        tests: [
          {
            name: "valid ages pass without throwing",
            code: 'const fn = new Function(code + "\\nreturn { validateAge, tryValidateAge, ValidationError };");\nconst { validateAge } = fn();\nvalidateAge(30);\nvalidateAge(0);',
            hint: "Only negative and non-number ages are invalid — 0 is a legal age.",
          },
          {
            name: "invalid ages throw a ValidationError",
            code: 'const fn = new Function(code + "\\nreturn { validateAge, tryValidateAge, ValidationError };");\nconst { validateAge, ValidationError } = fn();\nfor (const bad of [-1, "30", NaN]) {\n  let err;\n  try { validateAge(bad); } catch (e) { err = e; }\n  if (!err) throw new Error("validateAge(" + String(bad) + ") must throw.");\n  if (!(err instanceof ValidationError)) throw new Error("The thrown error must be a ValidationError instance, not a plain Error.");\n  if (err.name !== "ValidationError") throw new Error("Set this.name = \'ValidationError\' in the constructor.");\n}',
            hint: "typeof age !== 'number' || Number.isNaN(age) covers both bad-type and NaN cases.",
          },
          {
            name: "tryValidateAge returns result objects",
            code: 'const fn = new Function(code + "\\nreturn { validateAge, tryValidateAge, ValidationError };");\nconst { tryValidateAge } = fn();\nconst good = tryValidateAge(42);\nif (good.ok !== true || good.value !== 42) throw new Error("Success must return { ok: true, value: age }.");\nconst bad = tryValidateAge(-5);\nif (bad.ok !== false || !bad.error) throw new Error("Failure must return { ok: false, error } — not throw.");',
            hint: "Wrap validateAge in try/catch; on ValidationError return the error object, on anything else rethrow.",
          },
        ],
        vi: {
          title: "ValidationError tùy biến",
          prompt:
            'Định nghĩa `class ValidationError extends Error` với `name` là `"ValidationError"`. Viết `validateAge(age)` THROW một ValidationError với message `"age must be a number"` khi `age` không phải số (hoặc là NaN), và `"age must be non-negative"` khi nhỏ hơn 0. Viết `tryValidateAge(age)` RETURN `{ ok: true, value: age }` khi hợp lệ và `{ ok: false, error }` khi ValidationError bị ném ra — mọi lỗi khác vẫn phải được ném tiếp.',
          tests: [
            {
              name: "tuổi hợp lệ chạy qua không throw",
              hint: "Chỉ tuổi âm và không phải số là không hợp lệ — 0 là tuổi hợp lệ.",
            },
            {
              name: "tuổi không hợp lệ throw ValidationError",
              hint: "typeof age !== 'number' || Number.isNaN(age) phủ được cả sai kiểu lẫn NaN.",
            },
            {
              name: "tryValidateAge trả về result object",
              hint: "Bọc validateAge trong try/catch; gặp ValidationError thì trả về object lỗi, lỗi khác thì ném tiếp.",
            },
          ],
        },
      },
      {
        id: "i2-retry-once",
        title: "Retry on Failure",
        prompt:
          "Write `withRetry(task, retries)`. `task` is a zero-argument function. Call it; if it throws, call it again — up to `retries` additional attempts. RETURN the first successful result. If every attempt fails, rethrow the LAST error.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function withRetry(task, retries) {\n  // your code\n}\n",
        tests: [
          {
            name: "returns immediately when the task succeeds",
            code: 'const fn = new Function(code + "\\nreturn { withRetry };");\nconst { withRetry } = fn();\nlet calls = 0;\nconst out = withRetry(() => { calls++; return "done"; }, 3);\nif (out !== "done") throw new Error("The successful result must be returned.");\nif (calls !== 1) throw new Error("A task that succeeds first try must be called exactly once.");',
            hint: "Return the result inside the try block the moment the call succeeds.",
          },
          {
            name: "retries until success",
            code: 'const fn = new Function(code + "\\nreturn { withRetry };");\nconst { withRetry } = fn();\nlet calls = 0;\nconst out = withRetry(() => { calls++; if (calls < 3) throw new Error("flaky"); return "ok"; }, 3);\nif (out !== "ok") throw new Error("A task that fails twice then succeeds should return \'ok\'.");\nif (calls !== 3) throw new Error("The task should have been attempted 3 times (2 failures + 1 success).");',
            hint: "Loop attempts from 0 to retries inclusive; return early on the first success.",
          },
          {
            name: "rethrows the last error after exhausting retries",
            code: 'const fn = new Function(code + "\\nreturn { withRetry };");\nconst { withRetry } = fn();\nlet calls = 0;\nlet err;\ntry {\n  withRetry(() => { calls++; throw new Error("attempt " + calls); }, 2);\n} catch (e) { err = e; }\nif (!err) throw new Error("An always-failing task must eventually throw.");\nif (calls !== 3) throw new Error("Initial call + 2 retries = 3 attempts.");\nif (err.message !== "attempt 3") throw new Error("The rethrown error must be the LAST one (attempt 3), not the first.");',
            hint: "Remember the most recent error in a variable and throw it after the loop ends.",
          },
        ],
        vi: {
          title: "Thử lại khi thất bại",
          prompt:
            "Viết `withRetry(task, retries)`. `task` là một function không nhận đối số. Gọi nó; nếu nó throw, gọi lại — tối đa thêm `retries` lần nữa. RETURN kết quả của lần thành công đầu tiên. Nếu mọi lần thử đều thất bại, ném tiếp lỗi CUỐI CÙNG.",
          tests: [
            {
              name: "trả về ngay khi task thành công",
              hint: "Return kết quả ngay trong khối try ngay khi lời gọi thành công.",
            },
            {
              name: "thử lại cho đến khi thành công",
              hint: "Vòng lặp từ 0 đến retries (bao gồm cả hai đầu); return sớm ở lần thành công đầu tiên.",
            },
            {
              name: "ném tiếp lỗi cuối cùng sau khi hết lượt thử",
              hint: "Lưu lỗi gần nhất vào một biến rồi throw nó sau khi vòng lặp kết thúc.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-safe-parse",
      "function safeParse(json, fallback) {\n  try {\n    return JSON.parse(json);\n  } catch {\n    return fallback;\n  }\n}",
      "function safeParse(json, fallback) { return JSON.parse(json); }",
    ],
    [
      "i2-validation-error",
      'class ValidationError extends Error {\n  constructor(message) {\n    super(message);\n    this.name = "ValidationError";\n  }\n}\nfunction validateAge(age) {\n  if (typeof age !== "number" || Number.isNaN(age)) {\n    throw new ValidationError("age must be a number");\n  }\n  if (age < 0) {\n    throw new ValidationError("age must be non-negative");\n  }\n}\nfunction tryValidateAge(age) {\n  try {\n    validateAge(age);\n    return { ok: true, value: age };\n  } catch (err) {\n    if (err instanceof ValidationError) {\n      return { ok: false, error: err };\n    }\n    throw err;\n  }\n}',
      'class ValidationError extends Error {\n  constructor(message) {\n    super(message);\n    this.name = "ValidationError";\n  }\n}\nfunction validateAge(age) {\n  if (age < 0) {\n    return "age must be non-negative";\n  }\n}\nfunction tryValidateAge(age) {\n  return { ok: true, value: age };\n}',
    ],
    [
      "i2-retry-once",
      "function withRetry(task, retries) {\n  let last;\n  for (let attempt = 0; attempt <= retries; attempt++) {\n    try {\n      return task();\n    } catch (err) {\n      last = err;\n    }\n  }\n  throw last;\n}",
      "function withRetry(task, retries) { return task(); }",
    ],
  ],
);

// ── Practice: data-explorer-practice (mini build) ───────────────────────────
writePracticeSet(
  MOD,
  {
    file: "data-explorer-practice.json",
    id: "data-explorer-practice",
    title: "Mini Build: Data Explorer",
    description:
      "Build the explorer layer on top of the checkpoint core: a Map-backed index, a filter-sort-paginate query pipeline, and CSV export.",
    viTitle: "Dự án nhỏ: Trình khám phá dữ liệu",
    viDescription:
      "Xây tầng khám phá trên nền lõi của bài kiểm tra kiến thức: chỉ mục dựa trên Map, pipeline truy vấn lọc–sắp xếp–phân trang và xuất CSV.",
    afterLesson: "data-explorer-checkpoint",
    minutes: 25,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-explorer-index",
        title: "Explorer Index",
        prompt:
          "Write `createExplorer(records)` where each record has at least `{ id, score }`. It RETURNS an object with:\n\n- `byId(id)` — the record with that id, or `null` (build a Map once, up front)\n- `count()` — the number of records\n- `top(n)` — the first `n` records sorted by score, highest first; ties keep their original order; if there are fewer than `n`, return them all",
        difficulty: "intermediate",
        level: "guided",
        boilerplate: "function createExplorer(records) {\n  // your code\n}\n",
        tests: [
          {
            name: "byId finds records and returns null for unknown ids",
            code: 'const fn = new Function(code + "\\nreturn { createExplorer };");\nconst { createExplorer } = fn();\nconst ex = createExplorer([{ id: "a", score: 1 }, { id: "b", score: 2 }]);\nif (ex.byId("b")?.score !== 2) throw new Error("byId(\'b\') should return the record with id \'b\'.");\nif (ex.byId("zz") !== null) throw new Error("An unknown id must return null, not undefined.");',
            hint: "const index = new Map(records.map((r) => [r.id, r])); then index.get(id) ?? null.",
          },
          {
            name: "count returns the record count",
            code: 'const fn = new Function(code + "\\nreturn { createExplorer };");\nconst { createExplorer } = fn();\nconst ex = createExplorer([{ id: 1, score: 1 }, { id: 2, score: 2 }, { id: 3, score: 3 }]);\nif (ex.count() !== 3) throw new Error("count() should report the number of records (3 here).");',
            hint: "Just return records.length.",
          },
          {
            name: "top sorts by score desc and is stable for ties",
            code: 'const fn = new Function(code + "\\nreturn { createExplorer };");\nconst { createExplorer } = fn();\nconst recs = [\n  { id: 1, score: 5 },\n  { id: 2, score: 9 },\n  { id: 3, score: 5 },\n  { id: 4, score: 7 },\n];\nconst ex = createExplorer(recs);\nconst top2 = ex.top(2);\nif (top2.length !== 2 || top2[0].id !== 2 || top2[1].id !== 4) throw new Error("top(2) should be the two highest scores: ids 2 and 4.");\nconst topAll = ex.top(10);\nif (topAll.map((r) => r.id).join(",") !== "2,4,1,3") throw new Error("With ties (both score 5), the earlier record must come first: expected 2,4,1,3.");',
            hint: "Map records to { r, i } pairs, sort by (score desc, then index asc), slice, and unwrap.",
          },
        ],
        vi: {
          title: "Chỉ mục của trình khám phá",
          prompt:
            "Viết `createExplorer(records)` trong đó mỗi bản ghi có ít nhất `{ id, score }`. Hàm RETURN một object với:\n\n- `byId(id)` — bản ghi có id đó, hoặc `null` (dựng Map một lần ngay từ đầu)\n- `count()` — số bản ghi\n- `top(n)` — `n` bản ghi đầu tiên sắp theo điểm từ cao xuống thấp; bằng điểm thì giữ thứ tự gốc; nếu ít hơn `n` bản ghi thì trả về tất cả",
          tests: [
            {
              name: "byId tìm được bản ghi, trả null cho id lạ",
              hint: "const index = new Map(records.map((r) => [r.id, r])); rồi index.get(id) ?? null.",
            },
            { name: "count trả về số bản ghi", hint: "Chỉ cần return records.length." },
            {
              name: "top sắp điểm giảm dần và ổn định khi bằng điểm",
              hint: "Map bản ghi thành cặp { r, i }, sắp theo (điểm giảm, rồi index tăng), slice, rồi bóc lại.",
            },
          ],
        },
      },
      {
        id: "i2-explorer-query",
        title: "Query Pipeline",
        prompt:
          'Write `createQuery(records)` that RETURNS a function `query(opts)`. Each record has `{ id, score }`. `opts` may contain:\n\n- `minScore`, `maxScore` — inclusive score range; missing bounds are ignored\n- `sortBy` — `"score"` (default) or `"id"`\n- `order` — `"asc"` (default) or `"desc"`; ties keep original order\n- `page` (1-based, default 1), `perPage` (default 2)\n\n`query` RETURNS `{ items, total, page, pages }` where `items` is the current page of results (empty array when the page is out of range) and `pages` is `Math.ceil(total / perPage)` (0 when there are no results).',
        difficulty: "intermediate",
        level: "independent",
        boilerplate:
          "function createQuery(records) {\n  return function query(opts) {\n    // filter -> sort -> paginate\n  };\n}\n",
        tests: [
          {
            name: "filters by the inclusive score range",
            code: 'const fn = new Function(code + "\\nreturn { createQuery };");\nconst { createQuery } = fn();\nconst recs = [{ id: "a", score: 1 }, { id: "b", score: 5 }, { id: "c", score: 9 }];\nconst q = createQuery(recs);\nconst out = q({ minScore: 5, maxScore: 9 });\nif (out.total !== 2) throw new Error("Both bounds are inclusive: scores 5 and 9 must both survive (total 2).");\nif (q({}).total !== 3) throw new Error("With no bounds, every record passes the filter.");',
            hint: "Filter first: keep records where each present bound is satisfied with <= and >=.",
          },
          {
            name: "sorts by field and order, stably",
            code: 'const fn = new Function(code + "\\nreturn { createQuery };");\nconst { createQuery } = fn();\nconst recs = [\n  { id: "a", score: 5 },\n  { id: "b", score: 9 },\n  { id: "c", score: 5 },\n];\nconst q = createQuery(recs);\nconst desc = q({ sortBy: "score", order: "desc", perPage: 10 });\nif (desc.items.map((r) => r.id).join(",") !== "b,a,c") throw new Error("Score desc with ties: b (9) first, then a before c (stable).");\nconst idAsc = q({ sortBy: "id", perPage: 10 });\nif (idAsc.items.map((r) => r.id).join(",") !== "a,b,c") throw new Error("Sorting by id ascending gives a,b,c.");',
            hint: "Sort a copy — compare values, flip the sign for desc, and break ties with the original index.",
          },
          {
            name: "paginates and reports pages",
            code: 'const fn = new Function(code + "\\nreturn { createQuery };");\nconst { createQuery } = fn();\nconst recs = [\n  { id: "a", score: 1 }, { id: "b", score: 2 }, { id: "c", score: 3 },\n  { id: "d", score: 4 }, { id: "e", score: 5 },\n];\nconst q = createQuery(recs);\nconst p2 = q({ page: 2, perPage: 2 });\nif (p2.items.length !== 2 || p2.items[0].id !== "c") throw new Error("Page 2 of 5 records at 2 per page holds records 3 and 4 (ids c, d).");\nif (p2.total !== 5 || p2.pages !== 3 || p2.page !== 2) throw new Error("Expect total 5, pages 3, page 2.");\nconst far = q({ page: 9, perPage: 2 });\nif (far.items.length !== 0) throw new Error("A page beyond the range must return an empty items array.");\nif (createQuery([])({}).pages !== 0) throw new Error("Zero results means pages: 0.");',
            hint: "Slice with (page - 1) * perPage; pages is Math.ceil(total / perPage) but 0 for an empty set.",
          },
        ],
        vi: {
          title: "Pipeline truy vấn",
          prompt:
            'Viết `createQuery(records)` RETURN một function `query(opts)`. Mỗi bản ghi có `{ id, score }`. `opts` có thể chứa:\n\n- `minScore`, `maxScore` — khoảng điểm gồm cả hai đầu; biên bị bỏ qua nếu không truyền\n- `sortBy` — `"score"` (mặc định) hoặc `"id"`\n- `order` — `"asc"` (mặc định) hoặc `"desc"`; bằng giá trị thì giữ thứ tự gốc\n- `page` (bắt đầu từ 1, mặc định 1), `perPage` (mặc định 2)\n\n`query` RETURN `{ items, total, page, pages }` trong đó `items` là trang kết quả hiện tại (mảng rỗng khi page vượt phạm vi) và `pages` là `Math.ceil(total / perPage)` (bằng 0 khi không có kết quả).',
          tests: [
            {
              name: "lọc theo khoảng điểm gồm cả hai đầu",
              hint: "Lọc trước: giữ bản ghi thỏa mọi biên có mặt với <= và >=.",
            },
            {
              name: "sắp xếp theo trường và thứ tự, ổn định",
              hint: "Sắp trên một bản sao — so giá trị, đảo dấu cho desc, và hòa các kết quả bằng bằng index gốc.",
            },
            {
              name: "phân trang và báo số trang",
              hint: "Slice với (page - 1) * perPage; pages là Math.ceil(total / perPage) nhưng bằng 0 với tập rỗng.",
            },
          ],
        },
      },
      {
        id: "i2-explorer-export",
        title: "CSV Export",
        prompt:
          "Write `toCsv(records, columns)` that RETURNS a CSV string: the first line is `columns` joined by commas, then one line per record with the value for each column — an empty string when the record is missing that field. Numbers are stringified. No trailing newline.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function toCsv(records, columns) {\n  // your code\n}\n",
        tests: [
          {
            name: "header row matches the columns",
            code: 'const fn = new Function(code + "\\nreturn { toCsv };");\nconst { toCsv } = fn();\nconst out = toCsv([{ id: 1, name: "Ada" }], ["id", "name"]);\nif (out.split("\\n")[0] !== "id,name") throw new Error(\'The first line must be the columns joined by commas: "id,name".\');',
            hint: "Start with a lines array holding columns.join(',').",
          },
          {
            name: "missing fields become empty cells",
            code: 'const fn = new Function(code + "\\nreturn { toCsv };");\nconst { toCsv } = fn();\nconst out = toCsv([{ id: 1, name: "Ada" }, { id: 2 }], ["id", "name"]);\nif (out !== "id,name\\n1,Ada\\n2,") throw new Error(\'A record without name must render an empty cell: "id,name\\n1,Ada\\n2,".\');',
            hint: "Treat undefined and null as an empty string when mapping columns.",
          },
          {
            name: "numbers are stringified, no trailing newline",
            code: 'const fn = new Function(code + "\\nreturn { toCsv };");\nconst { toCsv } = fn();\nconst out = toCsv([{ id: 7, score: 9.5 }], ["id", "score"]);\nif (out !== "id,score\\n7,9.5") throw new Error(\'Numbers must become their string form: "id,score\\n7,9.5".\');\nif (out.endsWith("\\n")) throw new Error("No trailing newline after the last row.");',
            hint: "String(value) converts numbers; join lines with \\n, not an extra push.",
          },
        ],
        vi: {
          title: "Xuất CSV",
          prompt:
            "Viết `toCsv(records, columns)` RETURN một chuỗi CSV: dòng đầu tiên là `columns` nối bằng dấu phẩy, sau đó mỗi bản ghi một dòng với giá trị ứng từng cột — chuỗi rỗng khi bản ghi thiếu trường đó. Số được chuyển thành chuỗi. Không có ký tự xuống dòng cuối.",
          tests: [
            {
              name: "dòng header khớp với các cột",
              hint: "Bắt đầu với mảng lines chứa columns.join(',').",
            },
            {
              name: "trường thiếu thành ô rỗng",
              hint: "Xem undefined và null là chuỗi rỗng khi map qua các cột.",
            },
            {
              name: "số được chuyển thành chuỗi, không xuống dòng cuối",
              hint: "String(value) chuyển số; nối các dòng bằng \\n, đừng push thêm dòng rỗng.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-explorer-index",
      "function createExplorer(records) {\n  const index = new Map(records.map((r) => [r.id, r]));\n  return {\n    byId(id) {\n      return index.get(id) ?? null;\n    },\n    count() {\n      return records.length;\n    },\n    top(n) {\n      return records\n        .map((r, i) => ({ r, i }))\n        .sort((a, b) => b.r.score - a.r.score || a.i - b.i)\n        .slice(0, n)\n        .map((e) => e.r);\n    },\n  };\n}",
      "function createExplorer(records) {\n  return {\n    byId(id) { return undefined; },\n    count() { return records.length; },\n    top(n) { return records; },\n  };\n}",
    ],
    [
      "i2-explorer-query",
      'function createQuery(records) {\n  return function query(opts = {}) {\n    const { minScore, maxScore, sortBy = "score", order = "asc", page = 1, perPage = 2 } = opts;\n    let rows = records.filter(\n      (r) =>\n        (minScore === undefined || r.score >= minScore) &&\n        (maxScore === undefined || r.score <= maxScore),\n    );\n    rows = rows\n      .map((r, i) => ({ r, i }))\n      .sort((a, b) => {\n        const av = a.r[sortBy];\n        const bv = b.r[sortBy];\n        const cmp = av < bv ? -1 : av > bv ? 1 : 0;\n        const dir = order === "desc" ? -1 : 1;\n        return cmp * dir || a.i - b.i;\n      })\n      .map((e) => e.r);\n    const total = rows.length;\n    const pages = total === 0 ? 0 : Math.ceil(total / perPage);\n    const start = (page - 1) * perPage;\n    const items = rows.slice(start, start + perPage);\n    return { items, total, page, pages };\n  };\n}',
      "function createQuery(records) {\n  return function query(opts = {}) {\n    return { items: records, total: records.length, page: 1, pages: 1 };\n  };\n}",
    ],
    [
      "i2-explorer-export",
      'function toCsv(records, columns) {\n  const lines = [columns.join(",")];\n  for (const r of records) {\n    lines.push(\n      columns\n        .map((c) => (r[c] === undefined || r[c] === null ? "" : String(r[c])))\n        .join(","),\n    );\n  }\n  return lines.join("\\n");\n}',
      'function toCsv(records, columns) {\n  return columns.join(",");\n}',
    ],
  ],
);

console.log("Module 1 completion written.");
