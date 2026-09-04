/**
 * Author Module 4 (JavaScript Foundations) — script B: lessons 6–9.
 * Functions, scope & arrows, arrays, objects.
 *
 * Escaping-safe convention: NO raw backticks and NO raw "${" in content.
 * Backticks from T, dollars from D; code fences use ~~~.
 *
 * Run: node scripts/content-authoring/m4b.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const T = String.fromCharCode(96);
const D = String.fromCharCode(36);

const DIR =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/javascript-foundations/lessons";

function writeLesson(id, title, description, minutes, difficulty, challenges, mdx) {
  const lessonDir = path.join(DIR, id);
  mkdirSync(lessonDir, { recursive: true });
  writeFileSync(
    path.join(DIR, `${id}.json`),
    JSON.stringify(
      { id, title, description, minutes, difficulty, contentPath: `./${id}.mdx`, challenges },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(path.join(DIR, `${id}.mdx`), mdx.trimStart() + "\n");
  console.log("lesson:", id);
}

function writeChallenge(lessonId, challenge) {
  const dir = path.join(DIR, lessonId, "challenges");
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, `${challenge.id}.json`), JSON.stringify(challenge, null, 2) + "\n");
  console.log("  challenge:", challenge.id);
}

/* ── 4.6 Functions ───────────────────────────────────────────────────── */

writeLesson(
  "js-functions",
  "Functions: Reusable Code",
  "Wrap work in a name, feed it inputs, get an output back — the single most important structure in programming.",
  16,
  "beginner",
  ["temperature-converter", "function-practice"],
  `
You have already used functions: ${T}console.log${T} and
${T}name.toUpperCase()${T} are functions someone else wrote. Now you write your own.

## Declaring a function

~~~js
function greet(name) {
  return "Hello, " + name + "!";
}

greet("Ada")     // "Hello, Ada!"
greet("Grace")   // "Hello, Grace!" — same work, different input
~~~

Anatomy:

- ${T}function${T} — the keyword that starts a declaration
- ${T}greet${T} — the name (verb-like: functions *do* things)
- ${T}(name)${T} — **parameters**: named inputs the function expects
- ${T}return${T} — hands a value back to whoever called the function

## Parameters vs arguments

Parameters are the names in the definition; **arguments** are the actual values
passed in a call:

~~~js
function add(a, b) {     // a, b are parameters
  return a + b;
}

add(2, 3);               // 2 and 3 are arguments → 5
~~~

## return ends the function

The moment ${T}return${T} runs, the function is done — code below it is skipped.
A function with no ${T}return${T} gives back ${T}undefined${T}:

~~~js
function logTwice(msg) {
  console.log(msg);
  console.log(msg);
}                 // returns undefined — does work, hands nothing back

function double(n) {
  return n * 2;
}                 // hands 4 back when called with 2
~~~

Both styles are legitimate: *do something* (log, save, update the page) versus
*compute something* (return it). Graders in this course usually call your function,
so returning is how you hand results over.

## Why functions matter

Functions let you write logic **once** and trust it everywhere. Fix a bug inside
${T}greet${T} and every call site is fixed. They are also how bigger programs stay
readable: a well-named function is a one-line summary of what it does.

## What you learned

- Declare with ${T}function name(parameters) { ... }${T}
- ${T}return${T} hands a value back and ends the function
- No return → ${T}undefined${T}
- Write logic once, call it many times

**Next:** a shorter syntax for functions, and how variable visibility works.
`,
);

writeChallenge("js-functions", {
  id: "temperature-converter",
  title: "Temperature Converter",
  prompt:
    'Write a function `celsiusToFahrenheit(c)` that RETURNS the Fahrenheit equivalent — the formula is c * 9/5 + 32.\n\nThen log `celsiusToFahrenheit(0)` (should print 32) and `celsiusToFahrenheit(100)` (should print 212).',
  difficulty: "beginner",
  boilerplate: "// celsiusToFahrenheit(c) returns the converted temperature\n\n\n// log two conversions\n",
  tests: [
    {
      name: "converts correctly",
      code: `const fn = new Function(code + "\\nreturn { celsiusToFahrenheit };");
const { celsiusToFahrenheit } = fn();
if (celsiusToFahrenheit(0) !== 32) throw new Error("0°C should be 32°F.");
if (celsiusToFahrenheit(100) !== 212) throw new Error("100°C should be 212°F.");
if (celsiusToFahrenheit(37) !== 98.6) throw new Error("37°C should be 98.6°F — use the formula c * 9 / 5 + 32.");`,
      hint: "function celsiusToFahrenheit(c) { return c * 9 / 5 + 32; }",
    },
    {
      name: "logs both examples",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (!logs.some((l) => l === "32") || !logs.some((l) => l === "212")) {
  throw new Error("Log celsiusToFahrenheit(0) and celsiusToFahrenheit(100) — console should show 32 and 212.");
}`,
      hint: "console.log(celsiusToFahrenheit(0)); console.log(celsiusToFahrenheit(100));",
    },
  ],
});

writeChallenge("js-functions", {
  id: "function-practice",
  title: "Make a Greeter and a Max",
  prompt:
    '1. Write `greet(name)` that RETURNS a friendly sentence using the name (any sentence — build it with a template literal).\n2. Write `maxOfTwo(a, b)` that RETURNS whichever number is larger (if equal, return either).\n3. Log `greet("Ada")` and `maxOfTwo(7, 3)`.',
  difficulty: "beginner",
  boilerplate: "// 1) greet(name)\n\n\n// 2) maxOfTwo(a, b)\n\n\n// 3) log examples\n",
  tests: [
    {
      name: "greet builds a sentence with the name inside",
      code: `const fn = new Function(code + "\\nreturn { greet, maxOfTwo };");
const { greet } = fn();
const out = greet("Ada");
if (typeof out !== "string" || !out.includes("Ada")) {
  throw new Error('greet("Ada") must return a string containing "Ada".');
}
if (out === "Ada") {
  throw new Error("Return a full sentence, not just the name.");
}`,
      hint: "return `Hello, ${name}! welcome aboard.`; — any sentence works.",
    },
    {
      name: "maxOfTwo returns the larger",
      code: `const fn = new Function(code + "\\nreturn { greet, maxOfTwo };");
const { maxOfTwo } = fn();
if (maxOfTwo(7, 3) !== 7) throw new Error("maxOfTwo(7, 3) should be 7.");
if (maxOfTwo(2, 9) !== 9) throw new Error("maxOfTwo(2, 9) should be 9.");
if (maxOfTwo(5, 5) !== 5) throw new Error("maxOfTwo(5, 5) should be 5 (either is fine).");`,
      hint: "if (a >= b) { return a; } return b;  — or use the ternary a > b ? a : b",
    },
    {
      name: "examples logged",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (!logs.some((l) => l === "7")) {
  throw new Error("Log maxOfTwo(7, 3) — the console should show 7.");
}
if (!logs.some((l) => l.includes("Ada"))) {
  throw new Error("Log greet(\"Ada\") so the name appears in the console.");
}`,
      hint: "console.log(greet(\"Ada\")); console.log(maxOfTwo(7, 3));",
    },
  ],
});

/* ── 4.7 Scope & arrow functions ─────────────────────────────────────── */

writeLesson(
  "js-scope-and-arrows",
  "Scope and Arrow Functions",
  "Where variables live and who can see them — plus the shorter arrow syntax you will meet in every modern codebase.",
  14,
  "beginner",
  ["counter-factory"],
  `
## Scope: where a variable is visible

Variables declared inside a function exist **only inside it**:

~~~js
function calc() {
  const result = 42;    // born inside, dies inside
  return result;
}

console.log(result);    // ReferenceError — result is not visible out here
~~~

But the reverse works: a function can *read* variables declared **outside** it:

~~~js
const rate = 0.2;               // outer scope

function tax(amount) {
  return amount * rate;         // reads the outer variable
}
~~~

This is **scope**: inner sees outer, outer never sees inner. Keep most variables as
local as possible — a variable only one function needs belongs inside that function.

## Arrow functions — the shorter syntax

~~~js
const double = function (n) {
  return n * 2;
};

const doubleArrow = (n) => n * 2;     // identical behavior
~~~

An arrow function is an expression assigned to a variable. With **one expression**
after ${T}=>${T}, the value is returned automatically and the braces disappear.
With a **block body**, write ${T}return${T} yourself:

~~~js
const shout = (text) => text.toUpperCase() + "!";     // implicit return

const compare = (a, b) => {
  if (a === b) return 0;
  return a > b ? 1 : -1;
};                                                     // block body → explicit return
~~~

You will see both constantly. ${T}function${T} declarations are still perfect —
use whichever reads better; recognize both.

## Arrows in loops-over-data (a preview)

~~~js
const scores = [90, 72, 88];
scores.map((s) => s * 2);        // arrows are the natural fit here — arrays lesson next
~~~

## What you learned

- Inner scope sees outer variables; outer never sees inner
- Keep variables as local as possible
- Arrow: ${T}(params) => expression${T} (implicit return) or a block with ${T}return${T}

**Next:** arrays — working with lists of data.
`,
);

writeChallenge("js-scope-and-arrows", {
  id: "counter-factory",
  title: "Build a Counter",
  prompt:
    '1. Write a function `makeCounter()` that returns an object with two methods: `increment()` (adds 1) and `value()` (returns the current count). The count must start at 0 and be remembered between calls — a local variable inside makeCounter is the right home for it.\n2. Create `const counter = makeCounter();`, call `counter.increment()` twice, then log `counter.value()` — it should print 2.',
  difficulty: "intermediate",
  boilerplate: "// makeCounter() returns { increment, value }\n\n\n// create counter, increment twice, log the value\n",
  tests: [
    {
      name: "counter remembers state between calls",
      code: `const fn = new Function(code + "\\nreturn { makeCounter };");
const { makeCounter } = fn();
const c = makeCounter();
if (c.value() !== 0) throw new Error("A fresh counter should start at 0.");
c.increment();
c.increment();
if (c.value() !== 2) throw new Error("After two increments the value should be 2 — the count must be remembered between calls.");
c.increment();
if (c.value() !== 3) throw new Error("A third increment should make it 3.");
const c2 = makeCounter();
if (c2.value() !== 0) throw new Error("Each makeCounter() call should create an independent counter.");`,
      hint: "let count = 0; goes INSIDE makeCounter; return { increment: () => { count++; }, value: () => count };",
    },
    {
      name: "increment and value are functions",
      code: `const fn = new Function(code + "\\nreturn { makeCounter };");
const { makeCounter } = fn();
const c = makeCounter();
if (typeof c.increment !== "function") throw new Error("increment must be a function.");
if (typeof c.value !== "function") throw new Error("value must be a function.");`,
      hint: "return { increment: ..., value: ... } — both properties hold functions (methods).",
    },
    {
      name: "logs 2 after two increments",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (!logs.some((l) => l === "2")) {
  throw new Error("Log counter.value() after two increments — the console should show 2.");
}`,
      hint: "counter.increment(); counter.increment(); console.log(counter.value());",
    },
  ],
});

/* ── 4.8 Arrays ──────────────────────────────────────────────────────── */

writeLesson(
  "js-arrays",
  "Arrays: Lists of Values",
  "Store many values under one name, read any item by index, and meet the built-in methods that do heavy lifting.",
  16,
  "beginner",
  ["array-workout"],
  `
An **array** is an ordered list under one name:

~~~js
const skills = ["HTML", "CSS", "JavaScript"];
~~~

## Indexing — from zero

~~~js
skills[0]     // "HTML"       FIRST item is index 0
skills[2]     // "JavaScript"
skills[3]     // undefined    — beyond the end is not an error, just nothing
~~~

Arrays know their own length:

~~~js
skills.length   // 3
skills[skills.length - 1]   // last item — "JavaScript"
~~~

## Changing arrays

~~~js
const todos = ["learn HTML"];
todos.push("learn CSS");       // add to the END → length 2
todos.pop();                   // remove from the END → back to 1
~~~

## The workhorse methods

Each takes a function and builds a **new array** — the original is untouched:

~~~js
const scores = [90, 72, 88];

scores.map((s) => s * 2);          // [180, 144, 176] — transform each item
scores.filter((s) => s >= 80);     // [90, 88]        — keep passing items
scores.find((s) => s < 80);        // 72              — first match (or undefined)
scores.includes(88);               // true
scores.forEach((s) => console.log(s));   // runs the function per item, returns nothing
~~~

Read ${T}map${T} as *"one new item per old item"* and ${T}filter${T} as *"keep the
ones that pass"*. These two cover most list processing you will do this module.

## Looping an array — the classic pattern

~~~js
const names = ["Ada", "Grace", "Linus"];

for (let i = 0; i < names.length; i++) {
  console.log(i + ": " + names[i]);
}
~~~

Start at 0, keep going while ${T}i < names.length${T}. (Later:
${T}for...of${T} and ${T}forEach${T} shorten this — but read and write the classic
pattern fluently first.)

## What you learned

- Arrays: ordered lists; index from **0**; ${T}.length${T}
- ${T}push${T}/${T}pop${T} add/remove at the end
- ${T}map${T}, ${T}filter${T}, ${T}find${T}, ${T}includes${T}, ${T}forEach${T}
- Classic indexed loop over ${T}.length${T}

**Next:** objects — labeled data.
`,
);

writeChallenge("js-arrays", {
  id: "array-workout",
  title: "Array Workout",
  prompt:
    'Given `const scores = [45, 92, 67, 88, 30];` (declare it yourself):\n\n1. Write `passing(scoresArr)` that RETURNS a new array of only the scores >= 60.\n2. Write `toPercent(scoresArr)` that RETURNS a new array with each score doubled.\n3. Log how many scores are passing (use passing + .length).\n4. Log whether the list contains a 100 (use .includes).',
  difficulty: "intermediate",
  boilerplate:
    "const scores = [45, 92, 67, 88, 30];\n\n// 1) passing(scoresArr)\n\n\n// 2) toPercent(scoresArr)\n\n\n// 3) log the passing count\n\n// 4) log whether a 100 exists\n",
  tests: [
    {
      name: "passing filters to >= 60",
      code: `const fn = new Function(code + "\\nreturn { scores, passing, toPercent };");
const { passing } = fn();
const out = passing([45, 92, 67, 88, 30]);
const want = [92, 67, 88];
if (!Array.isArray(out) || out.length !== 3) throw new Error("passing should return 3 scores (92, 67, 88).");
if (JSON.stringify(out) !== JSON.stringify(want)) throw new Error("passing should return [92, 67, 88] in order.");`,
      hint: "const passing = (arr) => arr.filter((s) => s >= 60);",
    },
    {
      name: "toPercent doubles each score",
      code: `const fn = new Function(code + "\\nreturn { scores, passing, toPercent };");
const { toPercent } = fn();
const out = toPercent([2, 5]);
if (JSON.stringify(out) !== JSON.stringify([4, 10])) {
  throw new Error("toPercent([2, 5]) should be [4, 10] — transform each item with map.");
}`,
      hint: "const toPercent = (arr) => arr.map((s) => s * 2);",
    },
    {
      name: "count and includes logged",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (!logs.some((l) => l === "3")) {
  throw new Error("Log the passing count — the console should show 3.");
}
if (!logs.some((l) => l === "false")) {
  throw new Error("Log whether a 100 exists — the console should show false.");
}
if (!/.includes\\(/.test(code)) {
  throw new Error("Use .includes() to check for the 100.");
}`,
      hint: "console.log(passing(scores).length); console.log(scores.includes(100));",
    },
  ],
});

/* ── 4.9 Objects ─────────────────────────────────────────────────────── */

writeLesson(
  "js-objects",
  "Objects: Labeled Data",
  "Group related values under named keys, read and update them, and model real-world records — the shape behind every API.",
  16,
  "beginner",
  ["model-a-learner"],
  `
Arrays are numbered lists. **Objects** are labeled collections:

~~~js
const learner = {
  name: "Ada",
  streak: 12,
  level: "beginner",
};
~~~

Each ${T}key: value${T} pair is a **property**.

## Reading and writing properties

~~~js
learner.name          // "Ada"   — dot access (the default)
learner.streak        // 12
learner["name"]       // "Ada"   — bracket access (needed for dynamic keys)

learner.level = "confident beginner";   // update
learner.badges = ["first-run"];         // add a new property
~~~

## Methods — functions as properties

~~~js
const counter = {
  count: 0,
  increment() {
    this.count++;       // this = the object itself
  },
};

counter.increment();
counter.count;   // 1
~~~

A property whose value is a function is a **method**. Inside a method written this
way, ${T}this${T} refers to the object itself. Deep-dive later; recognize the shape
now.

## Objects + arrays: real data

Real page data is the combination:

~~~js
const lessons = [
  { title: "Variables", minutes: 10, done: true },
  { title: "Functions", minutes: 14, done: false },
  { title: "Arrays", minutes: 14, done: false },
];

lessons[1].title                  // "Functions" — index, then property
lessons.filter((l) => !l.done)    // the unfinished ones
lessons.find((l) => l.title === "Arrays")  // the whole object
~~~

Read compound expressions from the outside in. ${T}lessons[1].title${T}: the array →
item 1 → its title. This array-of-objects shape is what APIs return (Module 4's
final lessons) and what you will render into pages.

## JSON — the same shape as text

~~~js
const text = '{"name":"Ada","streak":12}';
const parsed = JSON.parse(text);   // string → object
JSON.stringify(learner);           // object → string
~~~

**JSON** (JavaScript Object Notation) is this data shape serialized as a string —
the lingua franca of web APIs. ${T}JSON.parse${T}/${T}stringify${T} convert both
ways; they return in the storage lesson too.

## What you learned

- Object literals: key/value pairs; dot access by default, brackets for dynamic keys
- Missing properties read as undefined; methods are function properties
- Arrays of objects model real data; compound access reads outside-in
- ${T}JSON.parse${T}/${T}stringify${T} bridge objects and strings

**Next:** the payoff — touching the actual page.
`,
);

writeChallenge("js-objects", {
  id: "model-a-learner",
  title: "Model a Learner",
  prompt:
    "Model real data:\n\n1. Create `learner` — an object with `name` (string), `streak` (number), and `skills` (an array of at least two skill names).\n2. Write `isOnFire(person)` that returns true when `streak` is 7 or more.\n3. Create `cohort` — an array of two learner objects (reuse the same shape). Log the name of the second one.",
  difficulty: "intermediate",
  boilerplate: "// 1) learner object\n\n// 2) isOnFire\n\n// 3) cohort + log\n",
  tests: [
    {
      name: "learner has the right shape",
      code: `const fn = new Function(code + "\\nreturn { learner, cohort, isOnFire };");
const { learner } = fn();
if (!learner || typeof learner.name !== "string" || learner.name.length === 0) {
  throw new Error("learner.name must be a non-empty string.");
}
if (typeof learner.streak !== "number") {
  throw new Error("learner.streak must be a number.");
}
if (!Array.isArray(learner.skills) || learner.skills.length < 2) {
  throw new Error("learner.skills must be an array with at least two entries.");
}`,
      hint: 'const learner = { name: "Ada", streak: 12, skills: ["HTML", "CSS"] };',
    },
    {
      name: "isOnFire reads the property",
      code: `const fn = new Function(code + "\\nreturn { learner, cohort, isOnFire };");
const { isOnFire } = fn();
if (isOnFire({ streak: 9 }) !== true) {
  throw new Error("A streak of 9 is on fire.");
}
if (isOnFire({ streak: 3 }) !== false) {
  throw new Error("A streak of 3 is not.");
}`,
      hint: "(person) => person.streak >= 7 — read the property off the parameter.",
    },
    {
      name: "cohort is an array of learners, second name logged",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
const fn = new Function("console", code + "\\nreturn { learner, cohort, isOnFire };");
const { cohort } = fn(fakeConsole);
if (!Array.isArray(cohort) || cohort.length < 2 || typeof cohort[1]?.name !== "string") {
  throw new Error("cohort must be an array of at least two learner-shaped objects.");
}
if (!logs.some((l) => l === cohort[1].name)) {
  throw new Error("Log the second learner's name (cohort[1].name).");
}`,
      hint: "console.log(cohort[1].name); — index into the array, then the property.",
    },
  ],
});
