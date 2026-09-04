/**
 * Author Module 4 (JavaScript Foundations) — script D: lessons 14–17.
 * localStorage, async/promises, fetch+APIs, JS checkpoint + project.
 *
 * Escaping-safe convention: NO raw backticks and NO raw "${" in content.
 * Backticks from T, dollars from D; code fences use ~~~.
 *
 * Run: node scripts/content-authoring/m4d.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const T = String.fromCharCode(96);

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

/* ── 4.14 localStorage & JSON ───────────────────────────────────────── */

writeLesson(
  "js-local-storage",
  "Browser Storage: localStorage + JSON",
  "Remember data between visits: localStorage persists in the browser, and JSON carries structured data in and out.",
  14,
  "intermediate",
  ["persist-a-preference"],
  `
Variables vanish when the page closes. **localStorage** gives every site a small,
private key–value store that survives reloads and restarts.

## The API — four methods

~~~js
localStorage.setItem("theme", "dark");      // save a string
localStorage.getItem("theme");               // "dark" — or null if absent
localStorage.removeItem("theme");            // delete one key
localStorage.clear();                        // delete everything for this site
~~~

Only **strings** are stored. Numbers, booleans, arrays, and objects must travel as
text — that is JSON's job:

~~~js
const settings = { theme: "dark", fontSize: 16 };

localStorage.setItem("settings", JSON.stringify(settings));     // object → string

const raw = localStorage.getItem("settings");
const parsed = JSON.parse(raw);                                  // string → object
parsed.fontSize;   // 16
~~~

## Guarding against corrupted data

${T}JSON.parse${T} throws on invalid text. Anything in storage could be old or
corrupted — wrap the read:

~~~js
function loadSettings() {
  try {
    return JSON.parse(localStorage.getItem("settings")) ?? { theme: "light" };
  } catch {
    return { theme: "light" };      // corrupted → fall back to defaults
  }
}
~~~

${T}?? ${T} (nullish coalescing) supplies a default when the left side is
${T}null${T}/${T}undefined${T} — perfect with ${T}getItem${T}, which returns
${T}null${T} for missing keys.

## What it is for — and what it is not

Great for: preferences, theme, drafts, "remember me" UI state, small game progress.

Not for: passwords or anything sensitive (any code on the page can read it), and not
for large data (a few MB at most). Real user accounts live on a server — localStorage
is the browser's notebook, not the database.

## A tiny state machine

~~~js
const visits = Number(localStorage.getItem("visits") ?? "0") + 1;
localStorage.setItem("visits", String(visits));
console.log("Visit number " + visits);
~~~

Read → update → write back — the same state-and-render loop as the counter, now
durable across visits.

## What you learned

- ${T}setItem${T}/${T}getItem${T}/${T}removeItem${T}/${T}clear${T}
- Storage holds strings: ${T}JSON.stringify${T} in, ${T}JSON.parse${T} out
- Wrap parses in try/catch; default missing values with ${T}??${T}
- Right tool for preferences and drafts — never for secrets

**Next:** programs that wait — asynchronous JavaScript.
`,
);

writeChallenge("js-local-storage", {
  id: "persist-a-preference",
  title: "Remember the Theme",
  prompt:
    'A `storage` object is provided that works like localStorage (setItem/getItem/removeItem).\n\n1. Write `saveSettings(settings)` that stores the settings object as JSON under the key "settings".\n2. Write `loadSettings()` that reads the key and RETURNS the parsed object — or the default { theme: "light" } when nothing is stored.\n3. Save { theme: "dark", fontSize: 16 }, then load it and log the theme — should print dark.',
  difficulty: "intermediate",
  boilerplate:
    '// storage works like localStorage: storage.setItem(k, v), storage.getItem(k)\n\n// 1) saveSettings(settings)\n\n// 2) loadSettings() — parsed object or { theme: "light" }\n\n// 3) save, load, log the theme\n',
  tests: [
    {
      name: "empty storage returns the default",
      code: `function makeStorage() { const m = new Map(); return { setItem: (k, v) => m.set(String(k), String(v)), getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null), removeItem: (k) => m.delete(String(k)) }; }
const storage = makeStorage();
const fn = new Function("storage", code + "\\nreturn { saveSettings, loadSettings };");
const { loadSettings } = fn(storage);
const out = loadSettings();
if (!out || out.theme !== "light") {
  throw new Error('loadSettings() with empty storage should return { theme: "light" }.');
}`,
      hint: 'const raw = storage.getItem("settings"); if (!raw) return { theme: "light" }; return JSON.parse(raw);',
    },
    {
      name: "save then load round-trips the object",
      code: `function makeStorage() { const m = new Map(); return { setItem: (k, v) => m.set(String(k), String(v)), getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null), removeItem: (k) => m.delete(String(k)) }; }
const storage = makeStorage();
const fn = new Function("storage", code + "\\nreturn { saveSettings, loadSettings };");
const { saveSettings, loadSettings } = fn(storage);
saveSettings({ theme: "dark", fontSize: 16 });
const out = loadSettings();
if (!out || out.theme !== "dark" || out.fontSize !== 16) {
  throw new Error("save then load should return { theme: \\"dark\\", fontSize: 16 } — JSON.stringify on save, JSON.parse on load.");
}`,
      hint: 'saveSettings: storage.setItem("settings", JSON.stringify(settings)); loadSettings: JSON.parse(storage.getItem("settings"))',
    },
    {
      name: "values are stored as JSON strings",
      code: `function makeStorage() { const m = new Map(); return { setItem: (k, v) => m.set(String(k), String(v)), getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null), removeItem: (k) => m.delete(String(k)) }; }
const storage = makeStorage();
const fn = new Function("storage", code + "\\nreturn { saveSettings, loadSettings };");
const { saveSettings } = fn(storage);
saveSettings({ theme: "dark" });
const raw = storage.getItem("settings");
if (typeof raw !== "string" || raw.indexOf("dark") === -1) {
  throw new Error("Objects must be stored via JSON.stringify — the raw value should be a JSON string.");
}`,
      hint: "storage.setItem(key, JSON.stringify(settings)); — storage only holds strings.",
    },
  ],
});

/* ── 4.15 Async: promises & async/await ─────────────────────────────── */

writeLesson(
  "js-async",
  "Asynchronous JavaScript: Promises and async/await",
  "Programs that wait: why JavaScript cannot pause, how promises model 'value later', and the async/await syntax that makes waiting readable.",
  18,
  "intermediate",
  ["sequence-with-await"],
  `
Some work takes time — network requests, timers. If JavaScript simply paused while
waiting, the whole page would freeze. Instead it is **asynchronous**: slow work
starts now, and its result arrives **later**.

## Callbacks and the problem

The oldest style passes a function to run when the work finishes:

~~~js
setTimeout(() => console.log("two seconds later"), 2000);
console.log("printed first");       // the timer's callback runs LATER
~~~

Fine for one step — but step A needing step B needing step C nests callbacks into an
unreadable pyramid. That pain is exactly what promises fix.

## Promises — a value that arrives later

A **promise** is an object representing work in progress. It is either
**pending**, **fulfilled** (with a value), or **rejected** (with an error):

~~~js
const p = fetchSomething();     // a promise — the value is not here yet

p.then((value) => console.log("got:", value));    // on success
p.catch((err) => console.log("failed:", err));    // on failure
~~~

## async/await — promises that read like normal code

Mark a function ${T}async${T} and you may ${T}await${T} promises inside it:

~~~js
async function showUser() {
  const response = await fetchUser();     // pause THIS function, not the page
  console.log(response.name);
}

showUser();
~~~

${T}await${T} suspends only the async function — the browser keeps rendering,
responding, scrolling. To the reader, async code now runs top to bottom.

## Error handling: try/catch

When an awaited promise rejects, the error surfaces as a thrown error — catch it:

~~~js
async function showUser() {
  try {
    const response = await fetchUser();
    console.log(response.name);
  } catch (err) {
    console.log("Could not load the user:", err.message);
  }
}
~~~

## Sequential vs parallel

~~~js
// one after another (when each step needs the previous):
const user = await getUser();
const posts = await getPosts(user.id);

// independent work can overlap — start all, await all:
const [a, b] = await Promise.all([getA(), getB()]);
~~~

## What you learned

- Slow work is asynchronous so the page never freezes
- Promises: pending → fulfilled/rejected; ${T}.then${T}/${T}.catch${T}
- ${T}async${T} functions can ${T}await${T}; rejections are caught with
  ${T}try/catch${T}
- ${T}Promise.all${T} overlaps independent work

**Next:** the most common async work of all — talking to servers.
`,
);

writeChallenge("js-async", {
  id: "sequence-with-await",
  title: "Await a Sequence",
  prompt:
    'A fake API is provided: `api.loadUser()` returns a promise resolving to { name: "Ada" }, and `api.loadGreeting(name)` returns a promise resolving to "Hello, <name>".\n\n1. Write an async function `run()` that awaits loadUser, then awaits loadGreeting with the user\'s name, and logs the final greeting.\n2. Call run().',
  difficulty: "intermediate",
  boilerplate:
    "// api.loadUser() and api.loadGreeting(name) return promises\n\n// 1) async function run()\n\n// 2) call run()\n",
  tests: [
    {
      name: "logs the awaited greeting",
      code: `const api = {
  loadUser: () => new Promise((res) => setTimeout(() => res({ name: "Ada" }), 5)),
  loadGreeting: (n) => new Promise((res) => setTimeout(() => res("Hello, " + n), 5)),
};
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
const fn = new Function("api", "console", code + "\\nreturn { run };");
const { run } = fn(api, fakeConsole);
await run();
await new Promise((r) => setTimeout(r, 20));
if (!logs.some((l) => l === "Hello, Ada")) {
  throw new Error('run() should await the user, await the greeting, and log "Hello, Ada" — got ' + JSON.stringify(logs) + ".");
}`,
      hint: "async function run() { const user = await api.loadUser(); const greeting = await api.loadGreeting(user.name); console.log(greeting); }",
    },
    {
      name: "uses await (not .then chains or raw promises)",
      code: `if (!/await\\s+api\\.loadUser|await\\s+\\w*\\.*loadUser/.test(code) && !/await\\s/.test(code)) {
  throw new Error("Use await inside your async function — that is the lesson.");
}`,
      hint: "The await keyword is the point of this exercise — no .then chains.",
    },
  ],
});

/* ── 4.16 fetch & APIs ──────────────────────────────────────────────── */

writeLesson(
  "js-fetch-and-apis",
  "Talking to Servers: fetch and APIs",
  "Ask a server for data with fetch, decode JSON, and handle the three outcomes every request has: success, failure, and slow.",
  18,
  "intermediate",
  ["load-and-display-user"],
  `
## What an API is

An **API** (Application Programming Interface) is a service's front door: a set of
URLs you can ask for data. A **web API** answers HTTP requests and replies —
usually in JSON. The weather number in your phone's app came from exactly this kind
of request.

## The request/response cycle

Your page (the **client**) sends an HTTP **request** to a URL; the server sends back
a **response** with a status code and a body:

- ${T}200${T} OK · ${T}201${T} Created · ${T}404${T} Not Found ·
  ${T}401${T} Unauthorized · ${T}500${T} Server error

${T}2xx${T} = success, ${T}4xx${T} = your request's fault, ${T}5xx${T} = the
server's fault. Learning to glance at status codes is a superpower — the network
tab in DevTools shows every request your page makes.

## fetch — the browser's request function

~~~js
const response = await fetch("https://api.example.com/users/1");

if (!response.ok) {          // ok is false for 4xx/5xx
  throw new Error("Request failed: " + response.status);
}

const user = await response.json();    // parse the JSON body
console.log(user.name);
~~~

Two awaits, two jobs: the first waits for the **headers** (status codes live here),
the second waits for and parses the **body** as JSON.

## The three outcomes every UI must handle

~~~js
async function loadUser() {
  try {
    const response = await fetch("/api/user");
    if (!response.ok) throw new Error("HTTP " + response.status);
    const user = await response.json();
    return user;                       // 1. success
  } catch (err) {
    return null;                       // 2. network/parse failure
  }
}
// 3. slow: show "Loading…" first, replace it when data lands
~~~

Real apps show a loading state, a useful error message, and only then the data.
Code Journey's own challenge runner does exactly this dance — you watch it every
time you press Run.

## GET and POST

${T}fetch${T} defaults to **GET** (get me data). To send data — a form submission,
a new record — add options:

~~~js
await fetch("/api/signup", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username: "ada" }),
});
~~~

## What you learned

- APIs are URLs that answer with data; JSON is the language
- ${T}fetch${T}: await headers, check ${T}response.ok${T}, await
  ${T}.json()${T}
- Handle success, failure, and slow — every time
- GET reads; POST sends (method + headers + body)

**Next:** the checkpoint — prove your JavaScript foundations.
`,
);

writeChallenge("js-fetch-and-apis", {
  id: "load-and-display-user",
  title: "Load a User from an API",
  prompt:
    'A fake `fetch` is provided that returns a promise resolving to a response object with `.ok` (true) and `.json()` (resolves to { name: "Ada", role: "learner" }).\n\n1. Write an async function `loadUser()` that awaits fetch("https://api.example.com/me"), checks response.ok (throw on failure), awaits response.json(), and RETURNS the parsed user object.\n2. Call loadUser() and log the returned user\'s name — should print Ada.',
  difficulty: "intermediate",
  boilerplate:
    '// fetch(url) resolves to { ok: true, json: async () => ({ name: "Ada", role: "learner" }) }\n\n// 1) async function loadUser()\n\n// 2) call it and log the name\n',
  tests: [
    {
      name: "returns the parsed user object",
      code: `function makeFetch() {
  return (url) => new Promise((res) => setTimeout(() => res({ ok: true, json: async () => ({ name: "Ada", role: "learner" }) }), 5));
}
const fetch = makeFetch();
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
const fn = new Function("fetch", "console", code + "\\nreturn { loadUser };");
const { loadUser } = fn(fetch, fakeConsole);
const user = await loadUser();
if (!user || user.name !== "Ada" || user.role !== "learner") {
  throw new Error("loadUser() should return the parsed object { name: \\"Ada\\", role: \\"learner\\" }.");
}`,
      hint: "const response = await fetch(url); if (!response.ok) throw new Error(...); return await response.json();",
    },
    {
      name: "checks response.ok and awaits json()",
      code: `if (!/\\.ok/.test(code)) {
  throw new Error("Check response.ok — fetch does not throw on 404/500 by itself.");
}
if (!/\\.json\\(\\)/.test(code)) {
  throw new Error("Parse the body with response.json().");
}`,
      hint: "if (!response.ok) throw new Error(...); — then response.json().",
    },
    {
      name: "logs the fetched name",
      code: `function makeFetch() {
  return (url) => new Promise((res) => setTimeout(() => res({ ok: true, json: async () => ({ name: "Ada", role: "learner" }) }), 5));
}
const fetch = makeFetch();
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("fetch", "console", code)(fetch, fakeConsole);
await new Promise((r) => setTimeout(r, 30));
if (!logs.some((l) => l === "Ada")) {
  throw new Error("Log the user's name after loading — the console should show Ada.");
}`,
      hint: "const user = await loadUser(); console.log(user.name);",
    },
  ],
});

/* ── 4.17 Checkpoint + project lesson ───────────────────────────────── */

writeLesson(
  "js-checkpoint",
  "Checkpoint: JavaScript Foundations",
  "Prove your fundamentals: variables, functions, arrays, objects, and async — a graded understanding check, not memorization.",
  15,
  "intermediate",
  ["js-fundamentals-checkpoint"],
  `
This checkpoint tests whether you can **use** the JavaScript you have learned —
prediction, small implementations, and one async step. If something fails, the test
names tell you exactly which concept to revisit.

## What it covers

- Variables and types (${T}const${T}/${T}let${T}, strings, numbers, booleans)
- Functions with parameters and returns
- Arrays and objects, including arrays of objects
- Working with promises and ${T}await${T}

Struggle here? Revisit the failing lesson, then retry — retaking a checkpoint is
normal practice, not defeat.

**After passing:** the module project — an interactive web app.
`,
);

writeChallenge("js-checkpoint", {
  id: "js-fundamentals-checkpoint",
  title: "JavaScript Fundamentals Check",
  prompt:
    'Build a small analytics helper — each step uses a different foundation:\n\n1. Write `average(numbers)` that RETURNS the mean of an array of numbers (empty array returns 0).\n2. Write `formatScore(name, score)` that RETURNS a template-literal sentence like "Ada scored 91".\n3. Write `bestLearner(learners)` that takes an array of { name, score } objects and RETURNS the whole object with the highest score.\n4. `checkReady()` is provided — it returns a promise resolving to true. Write an async function `announce()` that awaits it and returns the string "ready" when true.',
  difficulty: "intermediate",
  boilerplate:
    "// checkReady() is provided: returns a promise resolving to true\n\n// 1) average(numbers)\n\n// 2) formatScore(name, score)\n\n// 3) bestLearner(learners)\n\n// 4) async announce()\n",
  tests: [
    {
      name: "average handles normal and empty arrays",
      code: `const fn = new Function("checkReady", code + "\\nreturn { average, formatScore, bestLearner, announce };");
const { average } = fn();
if (average([2, 4, 6]) !== 4) throw new Error("average([2, 4, 6]) should be 4.");
if (average([5]) !== 5) throw new Error("average([5]) should be 5.");
if (average([]) !== 0) throw new Error("average([]) should return 0 — guard the empty case.");`,
      hint: "if (numbers.length === 0) return 0; then sum with a loop (or reduce) and divide by numbers.length.",
    },
    {
      name: "formatScore builds a template-literal sentence",
      code: `const fn = new Function("checkReady", code + "\\nreturn { average, formatScore, bestLearner, announce };");
const { formatScore } = fn();
const out = formatScore("Ada", 91);
if (out !== "Ada scored 91") {
  throw new Error('formatScore("Ada", 91) should return "Ada scored 91".');
}`,
      hint: "return `${name} scored ${score}`; — a template literal with both slots.",
    },
    {
      name: "bestLearner returns the highest-scoring object",
      code: `const fn = new Function("checkReady", code + "\\nreturn { average, formatScore, bestLearner, announce };");
const { bestLearner } = fn();
const data = [{ name: "Ada", score: 91 }, { name: "Grace", score: 97 }, { name: "Linus", score: 84 }];
const out = bestLearner(data);
if (!out || out.name !== "Grace" || out.score !== 97) {
  throw new Error("bestLearner should return the WHOLE object of the top scorer — { name: \\"Grace\\", score: 97 }.");
}`,
      hint: "Track the best-so-far in a loop, or sort a copy and return [0].",
    },
    {
      name: "announce awaits and returns the verdict",
      code: `const checkReady = () => new Promise((res) => setTimeout(() => res(true), 5));
const fn = new Function("checkReady", code + "\\nreturn { average, formatScore, bestLearner, announce };");
const { announce } = fn(checkReady);
const out = await announce();
if (out !== "ready") {
  throw new Error('announce() should await checkReady() and return "ready".');
}`,
      hint: 'async function announce() { const ok = await checkReady(); return ok ? "ready" : "not ready"; }',
    },
  ],
});

writeLesson(
  "js-project-interactive-app",
  "Project: Interactive Web App",
  "Combine DOM, events, state, localStorage, and fetch into one working app — a task tracker that remembers its data.",
  25,
  "intermediate",
  ["task-tracker-app"],
  `
Time to build something real. The **task tracker** is small but complete: real state,
real events, real persistence — the same architecture as production apps, at
beginner scale.

## Requirements

Build it inside one JavaScript program (the grader runs it with stubbed DOM and
storage — the logic is identical to the browser's):

1. **State:** a ${T}tasks${T} array of ${T}{ title, done }${T} objects, loaded
   from storage key ${T}"tasks"${T} (default: empty array).
2. **Add:** an ${T}addTask(title)${T} function that appends
   ${T}{ title, done: false }${T}, saves, and re-renders.
3. **Toggle:** a ${T}toggleTask(index)${T} function that flips
   ${T}done${T}, saves, and re-renders.
4. **Render:** a ${T}render()${T} function that empties the list element and
   creates one ${T}<li>${T} per task — text
   ${T}"[x] title"${T} for done tasks, ${T}"[ ] title"${T} otherwise.
5. **Flow:** add two tasks, toggle the first, and log each rendered item.

## Why each piece matters

- **State first:** ${T}tasks${T} is the single source of truth. Rendering is a
  pure projection of it — never edit list items by hand.
- **Persistence:** every state change calls save. Crash-proof by construction.
- **Render-after-change:** one render function, called everywhere. This is the
  exact pattern React later automates.

## Starting point

~~~js
const tasks = load();          // from storage (your loadSettings-style helper)

function save() { /* JSON.stringify into storage */ }
function render() { /* one li per task */ }
function addTask(title) { /* push, save, render */ }
function toggleTask(index) { /* flip, save, render */ }
~~~

Work through the functions in that order and test as you go — a working add before
you start on toggle.

**After this project:** how developers manage and share code — Git.
`,
);

writeChallenge("js-project-interactive-app", {
  id: "task-tracker-app",
  title: "Capstone: Task Tracker",
  prompt:
    'Build the task tracker. `storage` (localStorage-like) and `document` (records your DOM calls) are provided.\n\nRequirements:\n1. tasks load from storage key "tasks" as JSON (default: []).\n2. addTask(title) appends { title, done: false }, saves to storage, re-renders.\n3. toggleTask(index) flips done, saves, re-renders.\n4. render() creates one <li> per task inside the element with id "task-list": "[x] title" when done, "[ ] title" when not.\n5. Demonstrate: add "learn state", add "build tracker", toggle index 0.',
  difficulty: "intermediate",
  boilerplate:
    "// storage: setItem/getItem — document: createElement/querySelector/appendChild\n\n// load state\n\n// save()\n\n// render()\n\n// addTask(title)\n\n// toggleTask(index)\n\n// demo: two adds + one toggle\n",
  tests: [
    {
      name: "adds persist into storage as JSON",
      code: `function makeEnv() {
  const m = new Map();
  const storage = { setItem: (k, v) => m.set(String(k), String(v)), getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null) };
  function makeEl(tag) {
    const e = { tagName: String(tag).toUpperCase(), textContent: "", className: "", children: [], parent: null };
    e.appendChild = (c) => { c.parent = e; e.children.push(c); };
    e.remove = () => {};
    return e;
  }
  const list = makeEl("ul");
  const document = { createElement: (t) => makeEl(t), querySelector: (s) => (String(s).includes("task-list") ? list : null), getElementById: (id) => (id === "task-list" ? list : null) };
  return { storage, document, list, raw: () => storage.getItem("tasks") };
}
const env = makeEnv();
new Function("storage", "document", code)(env.storage, env.document);
const rawTasks = env.raw();
if (!rawTasks) throw new Error("Nothing was saved under the \\"tasks\\" key — save() must run on every change.");
const tasks = JSON.parse(rawTasks);
if (tasks.length !== 2) throw new Error("Expected 2 saved tasks — got " + tasks.length + ".");
if (tasks[0].title !== "learn state" || tasks[0].done !== true) throw new Error('Task 0 should be { title: "learn state", done: true } after the toggle.');
if (tasks[1].title !== "build tracker" || tasks[1].done !== false) throw new Error('Task 1 should be { title: "build tracker", done: false }.');`,
      hint: 'const tasks = JSON.parse(storage.getItem("tasks")) ?? [];  and  function save() { storage.setItem("tasks", JSON.stringify(tasks)); }',
    },
    {
      name: "render reflects state in the list",
      code: `function makeEnv() {
  const m = new Map();
  const storage = { setItem: (k, v) => m.set(String(k), String(v)), getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null) };
  function makeEl(tag) {
    const e = { tagName: String(tag).toUpperCase(), textContent: "", className: "", children: [], parent: null };
    e.appendChild = (c) => { c.parent = e; e.children.push(c); };
    e.remove = () => {};
    return e;
  }
  const list = makeEl("ul");
  const document = { createElement: (t) => makeEl(t), querySelector: (s) => (String(s).includes("task-list") ? list : null), getElementById: (id) => (id === "task-list" ? list : null) };
  return { storage, document, list };
}
const env = makeEnv();
new Function("storage", "document", code)(env.storage, env.document);
const texts = env.list.children.filter((c) => c.tagName === "LI").map((c) => c.textContent);
if (texts.length !== 2) throw new Error("render() should create one <li> per task — got " + texts.length + ".");
if (texts[0] !== "[x] learn state") throw new Error('The toggled task should render "[x] learn state" — got "' + texts[0] + '".');
if (texts[1] !== "[ ] build tracker") throw new Error('The open task should render "[ ] build tracker" — got "' + texts[1] + '".');`,
      hint: 'for (const t of tasks) { const li = document.createElement("li"); li.textContent = (t.done ? "[x] " : "[ ] ") + t.title; list.appendChild(li); }',
    },
  ],
});
