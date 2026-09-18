/**
 * Author Module 1 — modern-javascript (Course 2, Intermediate).
 * 7 lessons, 6 practice sets, 18 challenges, 1 checkpoint. EN + VI.
 *
 * Run: node scripts/content-authoring/i2-m1.mjs
 */
import { T, writeModule, writeLesson } from "./i2-lib.mjs";

const MOD = "modern-javascript";

writeModule(MOD, {
  title: "Modern JavaScript",
  summary:
    "The professional JavaScript layer: closures and modules, higher-order functions, Map/Set, destructuring, and error handling — applied through data transformation.",
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
    "destructuring-practice",
    "map-set-practice",
    "error-handling-practice",
    "data-explorer-practice",
  ],
});

/* ── 1.1 Scope & closures ─────────────────────────────────────────────── */

writeLesson(
  MOD,
  {
    id: "scope-closures",
    title: "Scope, Closures, and Why They Matter",
    description:
      "Execution context, the scope chain, and closures — the mechanism behind private state, factories, and half of modern JavaScript patterns.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
You have written functions for a while now. This lesson is about what happens
**around** them: where variables live, how inner functions reach outer
variables, and why a function can "remember" things after its parent has
finished running.

## Scope is a chain

Every function creates a new scope. When JavaScript looks up a name, it walks
outward through the **scope chain** — inner scope first, then outer scopes,
then globals:

~~~js
const rate = 0.2; // global scope

function subtotal(amount) {
  const fee = 1.5; // function scope
  return amount + fee; // finds fee here, amount as a parameter
}

function total(amount) {
  return subtotal(amount) * (1 + rate); // finds rate two scopes up
}
~~~

A variable declared in an inner scope **shadows** an outer one with the same
name — the inner one wins for everything inside it.

## Closures: functions with memory

When a function is created inside another function, it keeps a live reference
to the outer variables it uses — even after the outer function has returned.
That captured bundle is a **closure**:

~~~js
function makeCounter(start = 0) {
  let count = start; // captured by the returned function
  return {
    increment: () => ++count,
    value: () => count,
  };
}

const c = makeCounter();
c.increment(); // 1
c.increment(); // 2
const d = makeCounter(100); // a NEW closed-over count
d.value(); // 100 — c and d do not share state
~~~

Three things to notice:

- ${T}count${T} is invisible from outside — no ${T}c.count${T} — yet the returned
  functions can read and change it. That is **private state**.
- Each call to ${T}makeCounter${T} creates a fresh captured variable. Factories
  work because closures do not share.
- The variable lives as long as any function that captured it does.

## Where closures show up in real code

~~~js
// Event handler remembering configuration
function attachZoom(image, factor) {
  let zoomed = false;
  image.addEventListener("click", () => {
    zoomed = !zoomed; // the handler closes over zoomed and factor
    image.style.transform = zoomed ? "scale(" + factor + ")" : "none";
  });
}

// Once-only setup
function once(fn) {
  let done = false;
  return (...args) => {
    if (done) return;
    done = true;
    return fn(...args);
  };
}

// The classic setTimeout-in-a-loop question
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 3, 3, 3 — one shared var i
}
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 0, 1, 2 — a fresh binding per iteration
}
~~~

The loop example is the closure mechanic in miniature: ${T}let${T} creates a new
binding per iteration, so each timeout closes over its own \${T}i\${T}. With
\${T}var\${T} there is only one \${T}i\${T} for the whole loop, and by the time the
callbacks run it is 3.

## Why this matters at Intermediate

Closures are the implementation behind callbacks with state, module
namespacing, memoization, event handlers, and every "factory" you will meet —
including React hooks. From here on, "can you make it work" becomes "can you
**structure** it", and closures are the structuring tool.
`,
  },
  {
    title: "Scope, Closure và tầm quan trọng của chúng",
    description:
      "Execution context, chuỗi scope và closure — cơ chế đứng sau private state, factory và một nửa số pattern JavaScript hiện đại.",
    mdx: `
Bạn đã viết function được một thời gian. Bài này nói về điều xảy ra **xung
quanh** function: biến sống ở đâu, function bên trong truy cập biến bên ngoài
thế nào, và tại sao một function có thể "ghi nhớ" dữ liệu ngay cả sau khi
function cha đã chạy xong.

## Scope là một chuỗi

Mỗi function tạo ra một scope mới. Khi JavaScript tìm một tên biến, nó đi ra
ngoài qua **chuỗi scope** — scope trong cùng trước, rồi các scope bên ngoài,
cuối cùng là global:

~~~js
const rate = 0.2; // global scope

function subtotal(amount) {
  const fee = 1.5; // function scope
  return amount + fee; // tìm thấy fee ở đây, amount là tham số
}

function total(amount) {
  return subtotal(amount) * (1 + rate); // tìm rate cách hai tầng scope
}
~~~

Một biến khai báo trong scope bên trong sẽ **che (shadow)** biến cùng tên ở
ngoài — bên trong scope đó, biến trong thắng.

## Closure: function có trí nhớ

Khi một function được tạo bên trong function khác, nó giữ tham chiếu "sống"
tới các biến bên ngoài mà nó dùng — kể cả sau khi function ngoài đã return.
Phần dữ liệu được giữ lại đó là **closure**:

~~~js
function makeCounter(start = 0) {
  let count = start; // bị function trả về "bắt giữ"
  return {
    increment: () => ++count,
    value: () => count,
  };
}

const c = makeCounter();
c.increment(); // 1
c.increment(); // 2
const d = makeCounter(100); // một count MỚI hoàn toàn
d.value(); // 100 — c và d không chia sẻ state
~~~

Ba điều cần chú ý:

- ${T}count${T} vô hình từ bên ngoài — không tồn tại ${T}c.count${T} — nhưng
  các function trả về vẫn đọc và thay đổi được nó. Đó là **private state**.
- Mỗi lần gọi ${T}makeCounter${T} tạo một biến được bắt giữ mới. Factory hoạt
  động được là vì closure không dùng chung state.
- Biến tồn tại chừng nào còn có function nào giữ nó.

## Closure xuất hiện ở đâu trong code thực tế

~~~js
// Event handler nhớ cấu hình
function attachZoom(image, factor) {
  let zoomed = false;
  image.addEventListener("click", () => {
    zoomed = !zoomed; // handler đóng giữ zoomed và factor
    image.style.transform = zoomed ? "scale(" + factor + ")" : "none";
  });
}

// Setup chỉ chạy một lần
function once(fn) {
  let done = false;
  return (...args) => {
    if (done) return;
    done = true;
    return fn(...args);
  };
}

// Câu hỏi kinh điển: setTimeout trong vòng lặp
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 3, 3, 3 — một var i dùng chung
}
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 0, 1, 2 — mỗi vòng một binding riêng
}
~~~

Ví dụ vòng lặp chính là cơ chế closure ở dạng thu nhỏ: ${T}let${T} tạo một
binding mới mỗi vòng lặp, nên mỗi timeout giữ \${T}i\${T} của riêng nó. Với
\${T}var\${T} cả vòng lặp chỉ có một \${T}i\${T}, và đến lúc callback chạy thì nó
đã là 3.

## Vì sao điều này quan trọng ở Trung cấp

Closure là nền móng của callback có state, module, memoization, event handler
và mọi "factory" bạn sẽ gặp — kể cả React hooks. Từ đây, câu hỏi không còn là
"chạy được không" mà là "cấu trúc được không", và closure chính là công cụ
cấu trúc.
`,
  },
);

writePracticeSet(
  MOD,
  {
    file: "closures-practice.json",
    id: "closures-practice",
    title: "Closures — Practice",
    viTitle: "Closure — Luyện tập",
    description:
      "Build private state and factories with closures: a counter, a rate limiter, and a memoized function.",
    viDescription:
      "Dùng closure để tạo private state và factory: counter, rate limiter và hàm memoized.",
    afterLesson: "scope-closures",
    minutes: 15,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-make-counter",
        title: "Private Counter Factory",
        prompt:
          "Write a function `makeCounter()` that returns an object with two methods:\n\n- `increment()` — adds 1 to a private count and returns the new value\n- `value()` — returns the current count without changing it\n\nThe count must start at 0 and be completely inaccessible from outside — calling the factory twice must produce two independent counters.",
        difficulty: "intermediate",
        level: "guided",
        boilerplate: "function makeCounter() {\n  // your code\n}\n",
        tests: [
          {
            name: "counter counts up from 0",
            code: `const fn = new Function(code + "\\nreturn makeCounter;");
const { makeCounter } = fn();
const c = makeCounter();
c.increment(); c.increment(); c.increment();
if (c.value() !== 3) throw new Error("After three increments, value() should be 3.");`,
            hint: "Declare let count = 0 inside makeCounter, and let both returned methods close over it.",
          },
          {
            name: "count is private",
            code: `const fn = new Function(code + "\\nreturn makeCounter;");
const { makeCounter } = fn();
const c = makeCounter();
if ("count" in c) throw new Error("The count variable must not be reachable as c.count — keep it private via closure.");`,
            hint: "The variable lives inside makeCounter's scope — the returned methods are the only door.",
          },
          {
            name: "two counters are independent",
            code: `const fn = new Function(code + "\\nreturn makeCounter;");
const { makeCounter } = fn();
const a = makeCounter(); const b = makeCounter();
a.increment(); a.increment(); b.increment();
if (a.value() !== 2 || b.value() !== 1) throw new Error("Each factory call must create its own closed-over count.");`,
            hint: "If both counters share state, you probably stored count outside the function.",
          },
        ],
        vi: {
          title: "Factory Counter riêng tư",
          prompt:
            "Viết hàm `makeCounter()` trả về một object với hai method:\n\n- `increment()` — cộng 1 vào một biến đếm riêng tư và trả về giá trị mới\n- `value()` — trả về số đếm hiện tại mà không thay đổi nó\n\nBiến đếm phải bắt đầu từ 0 và hoàn toàn không truy cập được từ bên ngoài — gọi factory hai lần phải cho ra hai counter độc lập.",
          tests: [
            {
              name: "counter đếm tăng từ 0",
              hint: "Khai báo let count = 0 bên trong makeCounter, để cả hai method trả về cùng đóng giữ nó.",
            },
            {
              name: "biến đếm là riêng tư",
              hint: "Biến nằm trong scope của makeCounter — các method trả về là cánh cửa duy nhất.",
            },
            {
              name: "hai counter độc lập",
              hint: "Nếu hai counter dùng chung state, có lẽ bạn đặt count ở ngoài function.",
            },
          ],
        },
      },
      {
        id: "i2-rate-limiter",
        title: "Closure-Based Rate Limiter",
        prompt:
          "Write `createLimiter(maxCalls)` that returns a function. The returned function returns `true` the first `maxCalls` times it is invoked and `false` after that.\n\nExample with `createLimiter(2)`: `true, true, false, false, ...`\n\nThis is how click-debouncing and API throttling are usually structured — state captured in a closure, no globals.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function createLimiter(maxCalls) {\n  // your code\n}\n",
        tests: [
          {
            name: "allows first N calls then blocks",
            code: `const fn = new Function(code + "\\nreturn createLimiter;");
const { createLimiter } = fn();
const gate = createLimiter(2);
const results = [gate(), gate(), gate(), gate()];
if (JSON.stringify(results) !== JSON.stringify([true, true, false, false])) throw new Error("With maxCalls=2 expect true, true, false, false.");`,
            hint: "Keep a let allowed = maxCalls in the closure; decrement on each call and compare.",
          },
          {
            name: "each limiter has its own budget",
            code: `const fn = new Function(code + "\\nreturn createLimiter;");
const { createLimiter } = fn();
const a = createLimiter(1); const b = createLimiter(1);
a(); if (b() !== true) throw new Error("Exhausting limiter a must not affect limiter b.");`,
            hint: "State must be created inside createLimiter — per call, not shared.",
          },
        ],
        vi: {
          title: "Rate Limiter dựa trên Closure",
          prompt:
            "Viết `createLimiter(maxCalls)` trả về một function. Function đó trả về `true` trong `maxCalls` lần gọi đầu và `false` sau đó.\n\nVí dụ với `createLimiter(2)`: `true, true, false, false, ...`\n\nĐây chính là cấu trúc điển hình của click-debouncing và API throttling — state nằm trong closure, không có global.",
          tests: [
            {
              name: "cho N lần đầu rồi chặn",
              hint: "Giữ một let allowed = maxCalls trong closure; trừ đi sau mỗi lần gọi rồi so sánh.",
            },
            {
              name: "mỗi limiter có ngân sách riêng",
              hint: "State phải được tạo bên trong createLimiter — theo từng lần gọi, không dùng chung.",
            },
          ],
        },
      },
      {
        id: "i2-memoize",
        title: "Memoize with a Map",
        prompt:
          "Write `memoize(fn)` that returns a cached version of a single-argument function. Calling the returned function with an argument it has seen before must return the remembered result **without calling `fn` again**.\n\nStore previous results in a `Map` closed over by the wrapper.",
        difficulty: "intermediate",
        level: "combination",
        boilerplate: "function memoize(fn) {\n  // your code\n}\n",
        tests: [
          {
            name: "repeats return the cached result",
            code: `const fn = new Function(code + "\\nreturn memoize;");
const { memoize } = fn();
let calls = 0;
const slow = memoize((n) => { calls++; return n * 2; });
slow(4); slow(4); slow(4);
if (calls !== 1) throw new Error("fn should run once; the other calls must hit the cache.");
if (slow(4) !== 8) throw new Error("Cached value must equal the computed one.");`,
            hint: "const cache = new Map() inside memoize; check cache.has(key) before calling fn.",
          },
          {
            name: "different arguments compute separately",
            code: `const fn = new Function(code + "\\nreturn memoize;");
const { memoize } = fn();
let calls = 0;
const f = memoize((n) => { calls++; return n + 1; });
f(1); f(2);
if (calls !== 2) throw new Error("Two distinct arguments must each compute once.");`,
            hint: "Key the Map by the argument itself — that is exactly what Map is better at than a plain object.",
          },
        ],
        vi: {
          title: "Memoize bằng Map",
          prompt:
            "Viết `memoize(fn)` trả về phiên bản có cache của một function một tham số. Gọi function trả về với tham số đã gặp phải trả về kết quả đã nhớ **mà không gọi lại `fn`**.\n\nLưu kết quả cũ trong một `Map` được closure giữ lại.",
          tests: [
            {
              name: "lặp lại dùng kết quả cache",
              hint: "const cache = new Map() bên trong memoize; kiểm tra cache.has(key) trước khi gọi fn.",
            },
            {
              name: "tham số khác tính riêng",
              hint: "Dùng chính tham số làm key của Map — đúng điểm Map mạnh hơn object thường.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-make-counter",
      "function makeCounter() {\n  let count = 0;\n  return {\n    increment() { return ++count; },\n    value() { return count; },\n  };\n}",
      "function makeCounter() {\n  return { increment() { return 1; }, value() { return 0; } };\n}",
    ],
    [
      "i2-rate-limiter",
      "function createLimiter(maxCalls) {\n  let left = maxCalls;\n  return function () {\n    if (left > 0) { left--; return true; }\n    return false;\n  };\n}",
      "function createLimiter(maxCalls) { return function () { return true; }; }",
    ],
    [
      "i2-memoize",
      "function memoize(fn) {\n  const cache = new Map();\n  return function (arg) {\n    if (cache.has(arg)) return cache.get(arg);\n    const v = fn(arg);\n    cache.set(arg, v);\n    return v;\n  };\n}",
      "function memoize(fn) { return fn; }",
    ],
  ],
);

/* ── 1.2 Higher-order functions ───────────────────────────────────────── */

writeLesson(
  MOD,
  {
    id: "higher-order-functions",
    title: "Functions as Values: map, filter, reduce",
    description:
      "Callbacks, higher-order functions, and the functional toolkit — plus when a plain for-loop is the better choice.",
    minutes: 13,
    difficulty: "intermediate",
    mdx: `
In Beginner you *used* ${T}map${T} and ${T}filter${T}. Here we treat functions as
first-class values — the idea that makes those methods possible — and build
our own.

## Functions are values

A function can live in a variable, be passed to another function, and be
returned from one. A function that takes or returns functions is a
**higher-order function (HOF)**:

~~~js
// takes a function — HOF
function repeat(times, action) {
  for (let i = 0; i < times; i++) action(i);
}
repeat(3, (i) => console.log("run " + i));

// returns a function — HOF
const multiply = (a) => (b) => a * b;
const triple = multiply(3);
triple(4); // 12
~~~

## map / filter / reduce, precisely

~~~js
const orders = [
  { id: 1, user: "ada", total: 120, status: "paid" },
  { id: 2, user: "linh", total: 35, status: "open" },
  { id: 3, user: "ada", total: 80, status: "paid" },
];

// map: same length, transformed items
const totals = orders.map((o) => o.total); // [120, 35, 80]

// filter: subset, same shape
const paid = orders.filter((o) => o.status === "paid");

// reduce: any shape → any other shape
const byUser = orders.reduce((acc, o) => {
  acc[o.user] = (acc[o.user] ?? 0) + o.total;
  return acc;
}, {}); // { ada: 200, linh: 35 }
~~~

${T}reduce${T} deserves respect: it is the general-purpose one. ${T}map${T} and
${T}filter${T} can both be written with it, and so can grouping, counting, and
flattening. When a data question sounds like "combine everything into …",
reduce is the answer.

## Chaining and its limits

~~~js
const topAda = orders
  .filter((o) => o.user === "ada")
  .map((o) => o.total)
  .reduce((sum, t) => sum + t, 0); // 200
~~~

Chains read top-to-bottom like a pipeline. Two cautions:

- Each step copies the array. On hot paths over huge arrays, one ${T}for${T}
  loop beats three passes.
- A chain longer than ~5 steps is harder to read than two named steps.
  Refactoring into small named functions is the intermediate move:

~~~js
const paidFor = (user) => orders.filter((o) => o.user === user && o.status === "paid");
const sumTotals = (os) => os.reduce((s, o) => s + o.total, 0);
sumTotals(paidFor("ada")); // 200
~~~

## Why this matters at Intermediate

Data transformation is most of what applications do. The HOF toolkit — and
knowing when *not* to use it — is the difference between copy-pasting loops
and expressing intent.
`,
  },
  {
    title: "Function là giá trị: map, filter, reduce",
    description:
      "Callback, higher-order function và bộ công cụ functional — cùng lúc nào nên dùng vòng lặp thường thay thế.",
    mdx: `
Ở Sơ cấp bạn đã *dùng* ${T}map${T} và ${T}filter${T}. Ở đây ta coi function là
giá trị đầu tiên đúng nghĩa — ý tưởng làm nên các method đó — và tự viết lại.

## Function là một giá trị

Function có thể nằm trong biến, được truyền vào function khác, và được trả về
từ function khác. Function nhận hoặc trả về function gọi là
**higher-order function (HOF)**:

~~~js
// nhận một function — HOF
function repeat(times, action) {
  for (let i = 0; i < times; i++) action(i);
}
repeat(3, (i) => console.log("run " + i));

// trả về một function — HOF
const multiply = (a) => (b) => a * b;
const triple = multiply(3);
triple(4); // 12
~~~

## map / filter / reduce, chính xác

~~~js
const orders = [
  { id: 1, user: "ada", total: 120, status: "paid" },
  { id: 2, user: "linh", total: 35, status: "open" },
  { id: 3, user: "ada", total: 80, status: "paid" },
];

// map: cùng độ dài, biến đổi từng phần tử
const totals = orders.map((o) => o.total); // [120, 35, 80]

// filter: tập con, giữ nguyên hình dạng
const paid = orders.filter((o) => o.status === "paid");

// reduce: hình dạng bất kỳ → hình dạng bất kỳ khác
const byUser = orders.reduce((acc, o) => {
  acc[o.user] = (acc[o.user] ?? 0) + o.total;
  return acc;
}, {}); // { ada: 200, linh: 35 }
~~~

${T}reduce${T} đáng được nể trọng: nó là khái niệm tổng quát nhất. ${T}map${T} và
${T}filter${T} đều viết được bằng reduce, và cả grouping, counting, flattening
nữa. Khi câu hỏi dữ liệu nghe như "gộp tất cả thành …", reduce là câu trả lời.

## Chuỗi (chain) và giới hạn của nó

~~~js
const topAda = orders
  .filter((o) => o.user === "ada")
  .map((o) => o.total)
  .reduce((sum, t) => sum + t, 0); // 200
~~~

Chain đọc từ trên xuống như một đường ống. Hai điều cần cảnh giác:

- Mỗi bước sao chép mảng một lần. Với mảng khổng lồ chạy trong vòng lặp nóng,
  một vòng ${T}for${T} thắng ba lượt duyệt.
- Chain dài hơn ~5 bước khó đọc hơn hai bước có tên riêng. Refactor thành các
  function nhỏ có tên là bước đi đúng đắn ở trình độ trung cấp:

~~~js
const paidFor = (user) => orders.filter((o) => o.user === user && o.status === "paid");
const sumTotals = (os) => os.reduce((s, o) => s + o.total, 0);
sumTotals(paidFor("ada")); // 200
~~~

## Vì sao điều này quan trọng ở Trung cấp

Biến đổi dữ liệu chiếm phần lớn công việc của ứng dụng. Bộ công cụ HOF — và
biết khi nào *không* nên dùng — là ranh giới giữa copy-paste vòng lặp và
diễn đạt đúng ý định.
`,
  },
);

writePracticeSet(
  MOD,
  {
    file: "hof-practice.json",
    id: "hof-practice",
    title: "Transforming Data — Practice",
    viTitle: "Biến đổi dữ liệu — Luyện tập",
    description:
      "Chain map/filter/reduce over a realistic order list: totals, grouping, and a reusable pipeline.",
    viDescription:
      "Chuỗi map/filter/reduce trên danh sách đơn hàng thực tế: tổng, nhóm và pipeline tái sử dụng.",
    afterLesson: "higher-order-functions",
    minutes: 18,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-sum-by-user",
        title: "Group and Sum with reduce",
        prompt:
          "Given `orders` (an array of `{ user, total }` objects, already declared in the boilerplate), write `sumByUser(orders)` that RETURNS an object mapping each user to the sum of their totals.\n\nUse `reduce` — no `for` loops.",
        difficulty: "intermediate",
        level: "guided",
        boilerplate:
          'const orders = [\n  { user: "ada", total: 120 },\n  { user: "linh", total: 35 },\n  { user: "ada", total: 80 },\n];\n\nfunction sumByUser(orders) {\n  // your code\n}\n',
        tests: [
          {
            name: "returns correct grouped totals",
            code: `const fn = new Function(code + "\\nreturn sumByUser;");
const { sumByUser } = fn();
const out = sumByUser([{ user: "ada", total: 120 }, { user: "linh", total: 35 }, { user: "ada", total: 80 }]);
if (out.ada !== 200 || out.linh !== 35) throw new Error("Expected { ada: 200, linh: 35 }, got " + JSON.stringify(out));`,
            hint: "reduce with an empty object as the initial accumulator; add each total to acc[o.user].",
          },
          {
            name: "handles an empty list",
            code: `const fn = new Function(code + "\\nreturn sumByUser;");
const { sumByUser } = fn();
const out = sumByUser([]);
if (typeof out !== "object" || Array.isArray(out)) throw new Error("An empty list should return an empty object.");`,
            hint: "With no items, reduce returns the initial value — that is why the initial accumulator matters.",
          },
          {
            name: "uses reduce, not for loops",
            code: `if (/for\\s*\\(/.test(code)) throw new Error("Use reduce for this one — no for loops.");`,
            hint: "orders.reduce((acc, o) => { … return acc; }, {}) is the whole solution.",
          },
        ],
        vi: {
          title: "Nhóm và cộng bằng reduce",
          prompt:
            "Cho `orders` (mảng các object `{ user, total }`, đã khai báo sẵn trong boilerplate), viết `sumByUser(orders)` TRẢ VỀ một object ánh xạ mỗi user tới tổng đơn của họ.\n\nDùng `reduce` — không dùng vòng lặp `for`.",
          tests: [
            {
              name: "trả về tổng nhóm đúng",
              hint: "reduce với object rỗng làm accumulator ban đầu; cộng mỗi total vào acc[o.user].",
            },
            {
              name: "chấp nhận danh sách rỗng",
              hint: "Không có phần tử nào thì reduce trả về giá trị khởi tạo — vì vậy accumulator ban đầu quan trọng.",
            },
            {
              name: "dùng reduce, không dùng for",
              hint: "orders.reduce((acc, o) => { … return acc; }, {}) chính là toàn bộ lời giải.",
            },
          ],
        },
      },
      {
        id: "i2-pipeline",
        title: "Build a Reusable Pipeline",
        prompt:
          "Write two functions and compose them:\n\n- `topSpenders(orders, min)` — returns users whose order total is at least `min`, deduplicated, in first-seen order\n- `countBy(orders, keyFn)` — returns an object counting items by the key returned from `keyFn(item)`\n\nBoth must be built on `filter`/`map`/`reduce`.",
        difficulty: "intermediate",
        level: "combination",
        boilerplate:
          'const orders = [\n  { user: "ada", total: 120 },\n  { user: "linh", total: 35 },\n  { user: "ada", total: 80 },\n  { user: "sam", total: 200 },\n];\n\nfunction topSpenders(orders, min) {\n  // your code\n}\n\nfunction countBy(orders, keyFn) {\n  // your code\n}\n',
        tests: [
          {
            name: "topSpenders filters and dedupes",
            code: `const fn = new Function(code + "\\nreturn { topSpenders, countBy };");
const { topSpenders } = fn();
const orders = [{ user: "ada", total: 120 }, { user: "linh", total: 35 }, { user: "ada", total: 80 }, { user: "sam", total: 200 }];
const out = topSpenders(orders, 100);
if (JSON.stringify(out) !== JSON.stringify(["ada", "sam"])) throw new Error("Expected [ada, sam], got " + JSON.stringify(out));`,
            hint: "filter by total >= min, then map to user, then dedupe with a Set or reduce.",
          },
          {
            name: "countBy counts by derived key",
            code: `const fn = new Function(code + "\\nreturn { topSpenders, countBy };");
const { countBy } = fn();
const orders = [{ user: "ada", total: 120 }, { user: "linh", total: 35 }, { user: "ada", total: 80 }];
const out = countBy(orders, (o) => (o.total >= 100 ? "big" : "small"));
if (out.big !== 1 || out.small !== 2) throw new Error("Expected { big: 1, small: 2 }, got " + JSON.stringify(out));`,
            hint: "reduce with acc[key] = (acc[key] ?? 0) + 1.",
          },
        ],
        vi: {
          title: "Xây pipeline tái sử dụng",
          prompt:
            "Viết hai function và kết hợp chúng:\n\n- `topSpenders(orders, min)` — trả về các user có tổng đơn từ `min` trở lên, đã khử trùng lặp, theo thứ tự xuất hiện đầu tiên\n- `countBy(orders, keyFn)` — trả về object đếm số phần tử theo key mà `keyFn(item)` trả về\n\nCả hai phải xây trên `filter`/`map`/`reduce`.",
          tests: [
            {
              name: "topSpenders lọc và khử trùng lặp",
              hint: "filter theo total >= min, rồi map ra user, rồi khử trùng lặp bằng Set hoặc reduce.",
            },
            {
              name: "countBy đếm theo key suy ra",
              hint: "reduce với acc[key] = (acc[key] ?? 0) + 1.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-sum-by-user",
      'const orders = [\n  { user: "ada", total: 120 },\n  { user: "linh", total: 35 },\n  { user: "ada", total: 80 },\n];\n\nfunction sumByUser(orders) {\n  return orders.reduce((acc, o) => {\n    acc[o.user] = (acc[o.user] ?? 0) + o.total;\n    return acc;\n  }, {});\n}',
      "function sumByUser(orders) { return {}; }",
    ],
    [
      "i2-pipeline",
      "const orders = [];\nfunction topSpenders(orders, min) {\n  const seen = new Set();\n  return orders.filter((o) => o.total >= min).map((o) => o.user).filter((u) => { if (seen.has(u)) return false; seen.add(u); return true; });\n}\nfunction countBy(orders, keyFn) {\n  return orders.reduce((acc, o) => { const k = keyFn(o); acc[k] = (acc[k] ?? 0) + 1; return acc; }, {});\n}",
      "function topSpenders(orders, min) { return orders.map((o) => o.user); }\nfunction countBy(orders, keyFn) { return {}; }",
    ],
  ],
);

/* ── 1.3 Destructuring & spread ───────────────────────────────────────── */

writeLesson(
  MOD,
  {
    id: "destructuring-spread",
    title: "Destructuring, Spread, and Rest",
    description:
      "Unpack objects and arrays precisely, copy without aliasing bugs, and write flexible function signatures.",
    minutes: 11,
    difficulty: "intermediate",
    mdx: `
Intermediate JavaScript is full of function boundaries: API responses in,
options objects out, arrays merged. Destructuring and spread are the two
language features that make those boundaries clean.

## Object destructuring

~~~js
const response = { user: { name: "Ada", email: "ada@example.com" }, status: 200 };

const { user, status } = response; // pick two fields
const { name, email } = user; // or nest in one step:
const { user: { name: userName } } = response; // rename while unpacking
~~~

Destructuring in parameters is the professional default for options objects:

~~~js
function connect({ host, port = 5432, retries = 3 } = {}) {
  return host + ":" + port;
}
connect({ host: "db.local" }); // db.local:5432 — defaults kick in per-field
~~~

## Array destructuring

~~~js
const [first, second] = [10, 20];
const [head, ...tail] = [1, 2, 3, 4]; // head=1, tail=[2,3,4]
let a = 1, b = 2;
[a, b] = [b, a]; // swap without a temp
~~~

## Spread: copy and merge

The spread operator ${T}...${T} *expands* an iterable into a new context:

~~~js
const base = { theme: "dark", compact: false };
const userPrefs = { compact: true };
const settings = { ...base, ...userPrefs }; // later wins: { theme:"dark", compact:true }

const merged = [...arr1, ...arr2];
const copy = [...original]; // shallow copy — one level only!
~~~

**Shallow vs deep:** spread copies references one level deep. Nested objects
still alias:

~~~js
const a = { meta: { count: 1 } };
const b = { ...a };
b.meta.count = 99;
a.meta.count; // 99 — the inner object is shared
~~~

## Rest: collect instead of expand

Where spread expands, rest *collects*. Same syntax, opposite direction:

~~~js
function log(level, ...messages) { // rest parameter
  console.log("[" + level + "]", messages.join(" "));
}

const { id, ...rest } = user; // rest = user without id — great for stripping
~~~

A common real use — remove a field before sending data to an API:

~~~js
const { password, safeUser } = user; // wrong: destructures into password var
const { password: _omit, ...safeUser } = user; // right: everything else
~~~

## Why this matters at Intermediate

State updates (create a new object with one field changed), prop-passing,
and options handling all lean on these. They are also everywhere in the
framework code you will read later.
`,
  },
  {
    title: "Destructuring, Spread và Rest",
    description:
      "Giải nén object và array chính xác, sao chép không dính lỗi tham chiếu, và viết chữ ký function linh hoạt.",
    mdx: `
JavaScript trung cấp đầy ranh giới function: response API vào, options object
ra, array gộp lại. Destructuring và spread là hai tính năng ngôn ngữ giúp các
ranh giới đó sạch sẽ.

## Object destructuring

~~~js
const response = { user: { name: "Ada", email: "ada@example.com" }, status: 200 };

const { user, status } = response; // chọn hai field
const { name, email } = user; // hoặc lồng một bước:
const { user: { name: userName } } = response; // đổi tên khi giải nén
~~~

Destructuring trong tham số là chuẩn chuyên nghiệp cho options object:

~~~js
function connect({ host, port = 5432, retries = 3 } = {}) {
  return host + ":" + port;
}
connect({ host: "db.local" }); // db.local:5432 — default áp dụng theo từng field
~~~

## Array destructuring

~~~js
const [first, second] = [10, 20];
const [head, ...tail] = [1, 2, 3, 4]; // head=1, tail=[2,3,4]
let a = 1, b = 2;
[a, b] = [b, a]; // hoán đổi không cần biến tạm
~~~

## Spread: sao chép và gộp

Toán tử spread ${T}...${T} *trải* một iterable vào ngữ cảnh mới:

~~~js
const base = { theme: "dark", compact: false };
const userPrefs = { compact: true };
const settings = { ...base, ...userPrefs }; // cái sau thắng: { theme:"dark", compact:true }

const merged = [...arr1, ...arr2];
const copy = [...original]; // shallow copy — chỉ một tầng!
~~~

**Shallow vs deep:** spread chỉ sao chép tham chiếu một tầng. Object lồng bên
trong vẫn dùng chung:

~~~js
const a = { meta: { count: 1 } };
const b = { ...a };
b.meta.count = 99;
a.meta.count; // 99 — object bên trong bị chia sẻ
~~~

## Rest: thu thập thay vì trải

Spread trải ra, rest *gom vào*. Cùng cú pháp, ngược hướng:

~~~js
function log(level, ...messages) { // rest parameter
  console.log("[" + level + "]", messages.join(" "));
}

const { id, ...rest } = user; // rest = user không có id — tiện để strip field
~~~

Một use case thực tế phổ biến — bỏ một field trước khi gửi dữ liệu lên API:

~~~js
const { password, safeUser } = user; // sai: password thành biến riêng
const { password: _omit, ...safeUser } = user; // đúng: mọi thứ còn lại
~~~

## Vì sao điều này quan trọng ở Trung cấp

Cập nhật state (tạo object mới với một field đổi), truyền props, và xử lý
options đều dựa vào các cú pháp này. Chúng cũng xuất hiện khắp nơi trong code
framework bạn sẽ đọc sau này.
`,
  },
);

/* ── 1.4 Modules ───────────────────────────────────────────────────────── */

writeLesson(
  MOD,
  {
    id: "modules-import-export",
    title: "Modules: import/export and Code Organization",
    description:
      "ES modules, named vs default exports, barrel files, and how to split a growing script into maintainable files.",
    minutes: 12,
    difficulty: "intermediate",
    mdx: `
One file stops scaling fast. **ES modules** are JavaScript's built-in way to
split code into files with explicit dependencies.

## Named exports and imports

~~~js
// file: math-utils.js
export function clamp(n, min, max) {
  return Math.min(Math.max(n, min), max);
}
export const TAX_RATE = 0.1;

// file: app.js
import { clamp, TAX_RATE } from "./math-utils.js";
~~~

## Default export: one per module

~~~js
// file: logger.js
export default function log(msg) { console.log(msg); }

// file: app.js — the default can be named anything on import
import log from "./logger.js";
import whatever from "./logger.js"; // same thing
~~~

Rule of thumb: **default** for "the thing this module is about" (a component,
a class), **named** for utilities and constants. Named imports are greppable —
you can find every usage of ${T}clamp${T} across the codebase.

## Re-exports and barrel files

~~~js
// file: utils/index.js — a barrel
export { clamp } from "./math.js";
export { formatDate } from "./dates.js";

// consumers import from one place:
import { clamp, formatDate } from "./utils/index.js";
~~~

Barrels keep import paths tidy, but re-exporting everything from everything
creates circular-import bugs. Keep barrels shallow.

## Static vs dynamic

${T}import${T} statements are static: they run at load time and must be at the
top level. For code you want *later* (a heavy library used on one action),
use dynamic import — it returns a Promise:

~~~js
button.addEventListener("click", async () => {
  const { default: chart } = await import("./heavy-chart-lib.js");
  chart.render(data);
});
~~~

## Circular imports

When A imports B and B imports A, both can end up with ${T}undefined${T} during
startup. The fix is almost always extracting the shared piece into a third
module C that both import. If you see ${T}undefined is not a function${T} at
startup, check for a cycle.

## Why this matters at Intermediate

From here on you will structure multi-file programs: a data layer, a UI
layer, utilities. Modules are the unit of that structure — and the unit that
tests import.
`,
  },
  {
    title: "Module: import/export và tổ chức code",
    description:
      "ES module, named so với default export, barrel file, và cách tách script đang lớn dần thành nhiều file dễ bảo trì.",
    mdx: `
Một file sẽ nhanh chóng không còn đủ dùng. **ES module** là cách tích hợp sẵn
của JavaScript để tách code thành nhiều file với quan hệ phụ thuộc tường minh.

## Named export và import

~~~js
// file: math-utils.js
export function clamp(n, min, max) {
  return Math.min(Math.max(n, min), max);
}
export const TAX_RATE = 0.1;

// file: app.js
import { clamp, TAX_RATE } from "./math-utils.js";
~~~

## Default export: mỗi module một cái

~~~js
// file: logger.js
export default function log(msg) { console.log(msg); }

// file: app.js — default import có thể đặt tên tùy ý
import log from "./logger.js";
import whatever from "./logger.js"; // giống hệt
~~~

Nguyên tắc: **default** cho "thứ module này nói về" (một component, một
class), **named** cho tiện ích và hằng số. Named import tìm được bằng grep —
bạn lần ra mọi nơi dùng ${T}clamp${T} trong toàn codebase.

## Re-export và barrel file

~~~js
// file: utils/index.js — một barrel
export { clamp } from "./math.js";
export { formatDate } from "./dates.js";

// nơi dùng import từ một chỗ:
import { clamp, formatDate } from "./utils/index.js";
~~~

Barrel giúp đường import gọn, nhưng re-export hết mọi thứ từ mọi nơi sinh ra
bug import vòng. Giữ barrel nông.

## Static so với dynamic

Câu ${T}import${T} là static: chạy lúc nạp module và phải nằm ở cấp cao nhất.
Với code bạn chỉ cần *sau này* (thư viện nặng dùng trong một thao tác), dùng
dynamic import — nó trả về Promise:

~~~js
button.addEventListener("click", async () => {
  const { default: chart } = await import("./heavy-chart-lib.js");
  chart.render(data);
});
~~~

## Import vòng

Khi A import B và B import A, cả hai có thể nhận ${T}undefined${T} lúc khởi
động. Cách sửa gần như luôn là tách phần dùng chung ra module thứ ba mà cả
hai cùng import. Thấy ${T}undefined is not a function${T} lúc khởi động, hãy
kiểm tra vòng import.

## Vì sao điều này quan trọng ở Trung cấp

Từ đây bạn sẽ cấu trúc chương trình nhiều file: tầng dữ liệu, tầng giao
diện, tiện ích. Module là đơn vị của cấu trúc đó — và là đơn vị mà test
import vào.
`,
  },
);

writePracticeSet(
  MOD,
  {
    file: "modules-practice.json",
    id: "modules-practice",
    title: "Designing Module Boundaries — Practice",
    viTitle: "Thiết kế ranh giới module — Luyện tập",
    description:
      "Decide what a module exports, simulate a barrel file, and break a circular import.",
    viDescription: "Quyết định module export gì, mô phỏng barrel file, và gỡ một import vòng.",
    afterLesson: "modules-import-export",
    minutes: 12,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-design-module-api",
        title: "Design a Module's Public API",
        prompt:
          "Write a module object for a cart library. Define `createCart()` that returns an object exposing exactly three methods — `add(item)`, `total()`, `clear()` — and NO direct access to the items array.\n\n`add` accepts `{ name, price }` and returns the new item count. `total()` returns the sum of prices. `clear()` empties the cart.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function createCart() {\n  // your code\n}\n",
        tests: [
          {
            name: "add returns the running count",
            code: `const fn = new Function(code + "\\nreturn createCart;");
const { createCart } = fn();
const cart = createCart();
if (cart.add({ name: "pen", price: 2 }) !== 1) throw new Error("First add should return 1.");
if (cart.add({ name: "ink", price: 5 }) !== 2) throw new Error("Second add should return 2.");`,
            hint: "Keep items in a closure variable; return items.length after pushing.",
          },
          {
            name: "total sums prices",
            code: `const fn = new Function(code + "\\nreturn createCart;");
const { createCart } = fn();
const cart = createCart();
cart.add({ name: "pen", price: 2 }); cart.add({ name: "ink", price: 5 });
if (cart.total() !== 7) throw new Error("total() should be 7.");`,
            hint: "reduce over the closed-over items array.",
          },
          {
            name: "items array stays private",
            code: `const fn = new Function(code + "\\nreturn createCart;");
const { createCart } = fn();
const cart = createCart();
if ("items" in cart) throw new Error("The cart must not expose its items array directly.");`,
            hint: "Only the three methods belong on the returned object.",
          },
          {
            name: "clear resets count and total",
            code: `const fn = new Function(code + "\\nreturn createCart;");
const { createCart } = fn();
const cart = createCart();
cart.add({ name: "pen", price: 2 });
cart.clear();
if (cart.total() !== 0) throw new Error("After clear(), total() should be 0.");`,
            hint: "clear can reassign the closure variable to a fresh array.",
          },
        ],
        vi: {
          title: "Thiết kế API public của một module",
          prompt:
            "Viết một module object cho thư viện giỏ hàng. Định nghĩa `createCart()` trả về object chỉ expose đúng ba method — `add(item)`, `total()`, `clear()` — và KHÔNG cho truy cập trực tiếp mảng items.\n\n`add` nhận `{ name, price }` và trả về số phần tử mới. `total()` trả về tổng giá. `clear()` làm rỗng giỏ.",
          tests: [
            {
              name: "add trả về số lượng hiện tại",
              hint: "Giữ items trong biến closure; trả về items.length sau khi push.",
            },
            { name: "total cộng các giá", hint: "reduce trên mảng items được closure giữ lại." },
            {
              name: "mảng items được giữ riêng tư",
              hint: "Chỉ ba method được phép nằm trên object trả về.",
            },
            {
              name: "clear reset count và total",
              hint: "clear có thể gán lại biến closure thành mảng mới.",
            },
          ],
        },
      },
      {
        id: "i2-break-cycle",
        title: "Break a Circular Import",
        prompt:
          "Two modules depend on each other: `user.js` needs `formatName`, and `format.js` needs `getUser`. Write `extractShared(code)` — given a string describing the two modules, return the name of the piece that should move to a third shared module.\n\nActually, simpler and more real: write `findCycle(graph)` that detects a circular dependency. `graph` is an object mapping module name to an array of names it imports. Return `true` if any cycle exists, `false` otherwise.",
        difficulty: "intermediate",
        level: "combination",
        boilerplate: "function findCycle(graph) {\n  // your code\n}\n",
        tests: [
          {
            name: "detects a two-module cycle",
            code: `const fn = new Function(code + "\\nreturn findCycle;");
const { findCycle } = fn();
if (findCycle({ a: ["b"], b: ["a"] }) !== true) throw new Error("a→b→a is a cycle: expect true.");`,
            hint: "Walk the graph depth-first; if you reach a node already on the current path, that is a cycle.",
          },
          {
            name: "accepts an acyclic graph",
            code: `const fn = new Function(code + "\\nreturn findCycle;");
const { findCycle } = fn();
if (findCycle({ a: ["b", "c"], b: ["d"], c: ["d"], d: [] }) !== false) throw new Error("This graph has no cycle: expect false.");`,
            hint: "Track two sets: visited (done) and onPath (current recursion).",
          },
          {
            name: "handles self-import",
            code: `const fn = new Function(code + "\\nreturn findCycle;");
const { findCycle } = fn();
if (findCycle({ a: ["a"] }) !== true) throw new Error("A module importing itself is a cycle.");`,
            hint: "a→a means when you visit a and see a again on the current path.",
          },
        ],
        vi: {
          title: "Gỡ một import vòng",
          prompt:
            "Hai module phụ thuộc lẫn nhau: `user.js` cần `formatName`, còn `format.js` cần `getUser`. Viết `findCycle(graph)` để phát hiện phụ thuộc vòng. `graph` là object ánh xạ tên module tới mảng các module nó import. Trả về `true` nếu tồn tại chu trình, ngược lại `false`.",
          tests: [
            {
              name: "phát hiện chu trình hai module",
              hint: "Duyệt graph theo chiều sâu; nếu chạm node đã nằm trên đường đi hiện tại thì đó là chu trình.",
            },
            {
              name: "chấp nhận graph không có chu trình",
              hint: "Dùng hai tập: visited (đã xong) và onPath (đang đệ quy).",
            },
            {
              name: "xử lý self-import",
              hint: "a→a nghĩa là khi đang thăm a mà lại thấy a trên đường đi hiện tại.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-design-module-api",
      "function createCart() {\n  let items = [];\n  return {\n    add(item) { items.push(item); return items.length; },\n    total() { return items.reduce((s, i) => s + i.price, 0); },\n    clear() { items = []; },\n  };\n}",
      "function createCart() { return { items: [], add() { return 0; }, total() { return 0; }, clear() {} }; }",
    ],
    [
      "i2-break-cycle",
      "function findCycle(graph) {\n  const visited = new Set();\n  const onPath = new Set();\n  function visit(node) {\n    if (onPath.has(node)) return true;\n    if (visited.has(node)) return false;\n    visited.add(node); onPath.add(node);\n    for (const next of graph[node] ?? []) if (visit(next)) return true;\n    onPath.delete(node);\n    return false;\n  }\n  for (const node of Object.keys(graph)) if (visit(node)) return true;\n  return false;\n}",
      "function findCycle(graph) { return false; }",
    ],
  ],
);

/* ── 1.5 Map & Set ─────────────────────────────────────────────────────── */

writeLesson(
  MOD,
  {
    id: "map-set-structured-data",
    title: "Map, Set, and Structured Data",
    description:
      "When plain objects run out: Map for arbitrary keys and fast lookups, Set for uniqueness, and choosing the right structure.",
    minutes: 11,
    difficulty: "intermediate",
    mdx: `
Objects are great for records — a user, a config. But two jobs need
different tools: **keyed collections with non-string keys**, and
**uniqueness**.

## Map: a dictionary that accepts anything as a key

~~~js
const cache = new Map();
cache.set({ path: "/api/users" }, response); // an OBJECT as key!
cache.set(42, "answer");
cache.get({ path: "/api/users" }); // same reference → found

cache.has(key); // membership without retrieving
cache.delete(key);
cache.size; // number of entries
for (const [key, value] of cache) { ... } // iterates in insertion order
~~~

Two superpowers a plain object lacks:

- Keys can be any value — objects, functions, NaN.
- ${T}map.size${T} is O(1); ${T}Object.keys(obj).length${T} is not.

## WeakMap (a taste)

A ${T}WeakMap${T} holds keys *weakly*: if nothing else references a key
object, it can be garbage-collected along with its entry. Perfect for
attaching metadata to DOM nodes or library objects without leaking memory.

## Set: uniqueness as a data structure

~~~js
const emails = new Set();
emails.add("a@x.com");
emails.add("a@x.com"); // ignored — already present
emails.size; // 1

const unique = [...new Set(array)]; // dedupe an array in one line
emails.has("b@x.com"); // O(1) membership — faster than array.includes
~~~

## Choosing the structure

| Need | Use |
| --- | --- |
| Record with known fields | object |
| Keyed by dynamic/arbitrary keys, frequent add/remove | Map |
| Unique values, membership tests | Set |
| Ordered list | array |

Using an object as a lookup table with user-controlled keys has a security
wrinkle too: keys like ${T}__proto__${T} or ${T}constructor${T} can collide with
prototype properties. A Map is immune.

## Why this matters at Intermediate

Choosing data structures is an engineering decision. Reaching for the right
one — and knowing why — is exactly the "decide how to build this" skill this
course is about.
`,
  },
  {
    title: "Map, Set và dữ liệu có cấu trúc",
    description:
      "Khi object thường không đủ: Map cho key tùy ý và lookup nhanh, Set cho tính duy nhất, và cách chọn cấu trúc phù hợp.",
    mdx: `
Object rất hợp cho record — một user, một config. Nhưng có hai việc cần công
cụ khác: **bộ sưu tập có key không phải chuỗi**, và **tính duy nhất**.

## Map: từ điển nhận bất cứ thứ gì làm key

~~~js
const cache = new Map();
cache.set({ path: "/api/users" }, response); // một OBJECT làm key!
cache.set(42, "answer");
cache.get({ path: "/api/users" }); // cùng tham chiếu → tìm thấy

cache.has(key); // kiểm tra membership không cần lấy giá trị
cache.delete(key);
cache.size; // số phần tử
for (const [key, value] of cache) { ... } // duyệt theo thứ tự chèn
~~~

Hai siêu năng lực mà object thường thiếu:

- Key có thể là giá trị bất kỳ — object, function, NaN.
- ${T}map.size${T} là O(1); ${T}Object.keys(obj).length${T} thì không.

## WeakMap (mở đầu)

${T}WeakMap${T} giữ key *yếu*: nếu không còn gì tham chiếu tới object key,
nó sẽ bị dọn cùng entry của mình bởi garbage collector. Hoàn hảo để gắn
metadata vào DOM node hoặc object của thư viện mà không rò rỉ bộ nhớ.

## Set: tính duy nhất như một cấu trúc dữ liệu

~~~js
const emails = new Set();
emails.add("a@x.com");
emails.add("a@x.com"); // bị bỏ qua — đã có
emails.size; // 1

const unique = [...new Set(array)]; // khử trùng lặp mảng trong một dòng
emails.has("b@x.com"); // membership O(1) — nhanh hơn array.includes
~~~

## Chọn cấu trúc

| Nhu cầu | Dùng |
| --- | --- |
| Record với các field biết trước | object |
| Key động/tùy ý, thêm/xóa thường xuyên | Map |
| Giá trị duy nhất, kiểm tra membership | Set |
| Danh sách có thứ tự | array |

Dùng object làm bảng tra cứu với key do người dùng kiểm soát còn có một lỗ
hổng bảo mật: key như ${T}__proto__${T} hay ${T}constructor${T} có thể đụng
property của prototype. Map miễn nhiễm điều đó.

## Vì sao điều này quan trọng ở Trung cấp

Chọn cấu trúc dữ liệu là một quyết định kỹ thuật. Chạm đúng cấu trúc — và
biết vì sao — chính là kỹ năng "quyết định xây thế nào" mà khóa học này
hướng tới.
`,
  },
);

writePracticeSet(
  MOD,
  {
    file: "map-set-practice.json",
    id: "map-set-practice",
    title: "Choosing Structures — Practice",
    viTitle: "Chọn cấu trúc dữ liệu — Luyện tập",
    description:
      "Dedupe with Set, index with Map, and pick the right structure for three real lookups.",
    viDescription:
      "Khử trùng lặp bằng Set, đánh chỉ mục bằng Map, và chọn đúng cấu trúc cho ba bài toán tra cứu.",
    afterLesson: "map-set-structured-data",
    minutes: 14,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-dedupe-set",
        title: "Dedupe and Membership with Set",
        prompt:
          'Write `dedupeTags(tags)` that returns the unique tags of an array, preserving first-seen order, case-insensitively ("CSS" and "css" are the same tag; keep the first spelling seen). Also write `hasAll(tags, needed)` returning `true` only if every string in `needed` appears in `tags`.',
        difficulty: "intermediate",
        level: "guided",
        boilerplate:
          "function dedupeTags(tags) {\n  // your code\n}\n\nfunction hasAll(tags, needed) {\n  // your code\n}\n",
        tests: [
          {
            name: "dedupes case-insensitively keeping first spelling",
            code: `const fn = new Function(code + "\\nreturn { dedupeTags, hasAll };");
const { dedupeTags } = fn();
const out = dedupeTags(["CSS", "js", "css", "HTML", "js"]);
if (JSON.stringify(out) !== JSON.stringify(["CSS", "js", "HTML"])) throw new Error("Expected [CSS, js, HTML], got " + JSON.stringify(out));`,
            hint: "Track seen keys in a Set lowercased; push the original when not yet seen.",
          },
          {
            name: "hasAll checks every needed tag",
            code: `const fn = new Function(code + "\\nreturn { dedupeTags, hasAll };");
const { hasAll } = fn();
if (hasAll(["css", "js"], ["css"]) !== true) throw new Error("All present → true.");
if (hasAll(["css"], ["css", "js"]) !== false) throw new Error("Missing one → false.");`,
            hint: "Build a Set from tags once, then every() over needed with has().",
          },
          {
            name: "hasAll is efficient (uses Set, not nested loops)",
            code: `if (/\\.includes\\(.*\\.includes/.test(code)) throw new Error("Nested includes is O(n²) — build a Set instead.");`,
            hint: "const tagSet = new Set(tags); then needed.every((t) => tagSet.has(t)).",
          },
        ],
        vi: {
          title: "Khử trùng lặp và membership bằng Set",
          prompt:
            'Viết `dedupeTags(tags)` trả về các tag duy nhất của mảng, giữ thứ tự xuất hiện đầu tiên, không phân biệt hoa thường ("CSS" và "css" là một tag; giữ cách viết xuất hiện trước). Thêm `hasAll(tags, needed)` trả về `true` chỉ khi mọi chuỗi trong `needed` đều có trong `tags`.',
          tests: [
            {
              name: "khử trùng lặp không phân biệt hoa thường, giữ cách viết đầu",
              hint: "Theo dõi key đã thấy trong một Set viết thường; push bản gốc nếu chưa thấy.",
            },
            {
              name: "hasAll kiểm tra mọi tag cần thiết",
              hint: "Tạo Set từ tags một lần, rồi every() trên needed với has().",
            },
            {
              name: "hasAll hiệu quả (dùng Set, không lặp lồng)",
              hint: "const tagSet = new Set(tags); rồi needed.every((t) => tagSet.has(t)).",
            },
          ],
        },
      },
      {
        id: "i2-index-map",
        title: "Index a List with Map",
        prompt:
          "Write `indexById(users)` that returns a Map from each user's `id` to the user object, and `lookup(index, id)` that returns the user or `null` when absent.\n\nThen write `groupByRole(users)` returning a Map from role to an array of users with that role.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate:
          "function indexById(users) {\n  // your code\n}\n\nfunction lookup(index, id) {\n  // your code\n}\n\nfunction groupByRole(users) {\n  // your code\n}\n",
        tests: [
          {
            name: "index maps id to user; lookup misses return null",
            code: `const fn = new Function(code + "\\nreturn { indexById, lookup, groupByRole };");
const { indexById, lookup } = fn();
const users = [{ id: 1, name: "Ada", role: "admin" }, { id: 2, name: "Linh", role: "user" }];
const idx = indexById(users);
if (!(idx instanceof Map)) throw new Error("indexById must return a Map.");
if (lookup(idx, 2).name !== "Linh") throw new Error("lookup(idx, 2) should be Linh.");
if (lookup(idx, 99) !== null) throw new Error("Unknown id should return null.");`,
            hint: "new Map(users.map((u) => [u.id, u])) builds it in one expression.",
          },
          {
            name: "groupByRole buckets users",
            code: `const fn = new Function(code + "\\nreturn { indexById, lookup, groupByRole };");
const { groupByRole } = fn();
const users = [{ id: 1, name: "Ada", role: "admin" }, { id: 2, name: "Linh", role: "user" }, { id: 3, name: "Sam", role: "admin" }];
const g = groupByRole(users);
if (!(g instanceof Map)) throw new Error("groupByRole must return a Map.");
if (g.get("admin").length !== 2 || g.get("user").length !== 1) throw new Error("admin: 2 users, user: 1 user.");`,
            hint: "reduce into a Map: get the bucket with ?? [], push, set back.",
          },
        ],
        vi: {
          title: "Đánh chỉ mục danh sách bằng Map",
          prompt:
            "Viết `indexById(users)` trả về Map ánh xạ `id` của mỗi user tới object user, và `lookup(index, id)` trả về user hoặc `null` khi không có.\n\nSau đó viết `groupByRole(users)` trả về Map ánh xạ role tới mảng các user mang role đó.",
          tests: [
            {
              name: "index ánh xạ id sang user; lookup không thấy trả null",
              hint: "new Map(users.map((u) => [u.id, u])) xây nó trong một biểu thức.",
            },
            {
              name: "groupByRole chia nhóm user",
              hint: "reduce vào một Map: lấy bucket với ?? [], push, rồi set lại.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-dedupe-set",
      "function dedupeTags(tags) {\n  const seen = new Set();\n  const out = [];\n  for (const t of tags) {\n    const k = t.toLowerCase();\n    if (!seen.has(k)) { seen.add(k); out.push(t); }\n  }\n  return out;\n}\nfunction hasAll(tags, needed) {\n  const s = new Set(tags.map((t) => t.toLowerCase()));\n  return needed.every((t) => s.has(t.toLowerCase()));\n}",
      "function dedupeTags(tags) { return tags; }\nfunction hasAll(tags, needed) { return false; }",
    ],
    [
      "i2-index-map",
      "function indexById(users) { return new Map(users.map((u) => [u.id, u])); }\nfunction lookup(index, id) { return index.get(id) ?? null; }\nfunction groupByRole(users) {\n  const m = new Map();\n  for (const u of users) {\n    const bucket = m.get(u.role) ?? [];\n    bucket.push(u);\n    m.set(u.role, bucket);\n  }\n  return m;\n}",
      "function indexById(users) { return new Map(); }\nfunction lookup(index, id) { return undefined; }\nfunction groupByRole(users) { return new Map(); }",
    ],
  ],
);
