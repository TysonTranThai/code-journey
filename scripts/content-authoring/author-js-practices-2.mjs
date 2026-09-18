/**
 * Author DOM/API practice content (Course 1 revision, wave 3 part 2).
 * DOM + event + storage + async challenges, with the standard stubs.
 *
 * Run: node scripts/content-authoring/author-js-practices-2.mjs
 */
import { mkdirSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const BASE =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/javascript-foundations/practices";
const SOLUTIONS_FILE = "scripts/content-authoring/practice-solutions.mjs";
const P = (id) => path.join(BASE, id, "challenges");

const SETS = [
  {
    file: "js-dom-practice.json",
    id: "js-dom-practice",
    title: "DOM Practice Gym",
    description:
      "Select, change, create: update text and classes from JS, render a list from an array, and wire a counter button.",
    afterLesson: "js-dom-select",
    minutes: 16,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-dom-text-and-class",
        title: "Update Text and Class",
        prompt: `The page gives you \`heading\` (an \`h1\` element) and \`intro\` (a \`p\` element). In JS:
- Set \`heading\`'s text to \`Pipeline running\`.
- Add the class \`is-active\` to \`intro\`.

Rules:
- Use \`textContent\` and \`classList.add\`.`,
        difficulty: "beginner",
        boilerplate:
          'const heading = document.getElementById("heading");\nconst intro = document.getElementById("intro");\n// update them\n',
        tests: [
          {
            name: "heading text updated",
            code: `if (!/heading\\.textContent\\s*=\\s*["']Pipeline running["']/.test(code)) {
  throw new Error("Set heading.textContent to 'Pipeline running'.");
}`,
            hint: 'heading.textContent = "Pipeline running"; — textContent is the safe way to set text.',
          },
          {
            name: "class added via classList",
            code: `if (!/intro\\.classList\\.add\\s*\\(\\s*["']is-active["']\\s*\\)/.test(code)) {
  throw new Error("Add the class: intro.classList.add('is-active').");
}`,
            hint: 'intro.classList.add("is-active") — add, don\'t overwrite className.',
          },
        ],
      },
      {
        id: "practice-dom-create-items",
        title: "Render a List from Data",
        prompt: `Given \`const todos = ["learn the DOM", "build a list", "render from data"]\` and the \`#todo-list\` element: create one \`li\` per todo (with \`createElement\` + \`textContent\`), and append each to the list.

Rules:
- Loop or forEach over the array.
- Every li's text comes from the data.`,
        difficulty: "beginner",
        boilerplate: `const todos = ["learn the DOM", "build a list", "render from data"];
const list = document.querySelector("#todo-list");
// create and append one li per todo
`,
        tests: [
          {
            name: "creates list items",
            code: `if (!/document\\.createElement\\s*\\(\\s*["']li["']\\s*\\)/.test(code)) {
  throw new Error("Create <li> elements with document.createElement('li').");
}`,
            hint: 'const li = document.createElement("li"); inside your loop.',
          },
          {
            name: "text comes from the data",
            code: `if (!/\\.textContent\\s*=/.test(code)) throw new Error("Set each li's textContent from the todo.");`,
            hint: "li.textContent = todo; — the loop variable carries the data.",
          },
          {
            name: "items appended to the list",
            code: `if (!/list\\.appendChild\\s*\\(\\s*li\\s*\\)/.test(code)) {
  throw new Error("Append each li: list.appendChild(li).");
}`,
            hint: "list.appendChild(li) attaches the new element to the page.",
          },
        ],
      },
      {
        id: "practice-dom-counter",
        title: "Wire a Counter Button",
        prompt: `You have \`button\` (a button element) and \`display\` (a span). Make the button clicks count: keep a \`count\` variable, listen for \`click\`, and show the new value in \`display\` on every click. Then simulate two clicks by calling the handler logic twice, and log the display text (should be \`2\`).

Rules:
- \`addEventListener("click", …)\` on the button.
- The display updates inside the handler.`,
        difficulty: "beginner",
        boilerplate:
          "let count = 0;\n// listen for clicks and update display\n// then simulate: call the handler twice, log display.textContent\n",
        tests: [
          {
            name: "click listener registered",
            code: `if (!/button\\.addEventListener\\s*\\(\\s*["']click["']/.test(code)) {
  throw new Error("Listen for clicks: button.addEventListener('click', handler).");
}`,
            hint: 'button.addEventListener("click", bump);',
          },
          {
            name: "display updates inside the handler",
            code: `const handler = code.match(/(?:function\\s+(\\w+)|(?:const|let)\\s+(\\w+)\\s*=\\s*(?:\\([^)]*\\)|\\w+)\\s*=>)/);
const name = handler ? (handler[1] ?? handler[2]) : null;
if (!name) throw new Error("Define a named handler function.");
const body = code.match(new RegExp(\`(?:function\\\\\\\\s+\\\${name}[^\\\\\\\\{]*\\\\\\\\{[\\\\\\\\s\\\\\\\\S]*?\\\\\\\\n\\\\\\\\}|(?:const|let)\\\\\\\\s+\\\${name}[^=]*=>[\\\\\\\\s\\\\\\\\S]*?\\\\\\\\n\\\\\\\\})\`));
if (!/display\\.textContent\\s*=/.test(code)) throw new Error("Update display.textContent inside the handler.");`,
            hint: "The handler body must include display.textContent = count; (after incrementing).",
          },
          {
            name: "two simulated clicks show 2",
            code: `const m = code.match(/display\\.textContent\\s*=\\s*(\\w+)/);
const varName = m ? m[1] : "count";
const fn = new Function(code + "\\nreturn display;");
const d = fn();
if (String(d.textContent) !== "2") throw new Error("After two clicks the display should show 2.");`,
            hint: "Call the handler twice, then log display.textContent — it should read 2.",
          },
        ],
      },
    ],
  },
  {
    file: "js-storage-practice.json",
    id: "js-storage-practice",
    title: "State That Survives",
    description:
      "Persistence with localStorage: save objects as JSON, load them back safely, and handle corrupt data like a professional.",
    afterLesson: "js-local-storage",
    minutes: 12,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-storage-roundtrip",
        title: "Save and Load Settings",
        prompt: `Write \`saveSettings(settings)\` that stores the object under key \`"settings"\` as JSON, and \`loadSettings()\` that reads it back and returns the object (default \`{ theme: "light" }\` when nothing is stored). Save \`{ theme: "dark", fontSize: 16 }\`, then log the loaded theme (should be \`dark\`).

Rules:
- \`storage\` is provided (same API as localStorage).
- JSON.stringify on the way in, JSON.parse on the way out.`,
        difficulty: "beginner",
        boilerplate:
          'function saveSettings(settings) {\n  // stringify and store\n}\nfunction loadSettings() {\n  // read, parse, default\n}\nsaveSettings({ theme: "dark", fontSize: 16 });\nconsole.log(loadSettings().theme);\n',
        tests: [
          {
            name: "objects are stringified before storing",
            code: `if (!/JSON\\.stringify/.test(code)) {
  throw new Error("localStorage stores strings — JSON.stringify the object first.");
}`,
            hint: 'storage.setItem("settings", JSON.stringify(settings));',
          },
          {
            name: "load parses and returns the object",
            code: `const fn = new Function(code + "\\nreturn loadSettings();");
const s = fn();
if (!s || s.theme !== "dark" || s.fontSize !== 16) {
  throw new Error("loadSettings() should return { theme: 'dark', fontSize: 16 }.");
}`,
            hint: 'Read with storage.getItem("settings"), then JSON.parse it.',
          },
          {
            name: "empty storage gets the default",
            code: `const fn = new Function(code + "; storage.removeItem('settings'); return loadSettings();");
const s = fn();
if (!s || s.theme !== "light") throw new Error("With nothing stored, loadSettings() should return { theme: 'light' }.");`,
            hint: "When getItem returns null, return the default object instead of parsing null.",
          },
        ],
      },
      {
        id: "practice-storage-corrupt-guard",
        title: "Debug: Survive Corrupt Data",
        prompt: `This loader crashes when the stored value isn't valid JSON. Add a \`try/catch\` around the parse: on failure, return the default \`{ theme: "light" }\`. Test by storing garbage (\`"not-json{{"\`) and loading — it must return the default instead of throwing.

Rules:
- try/catch around JSON.parse.
- The catch returns the default.`,
        difficulty: "beginner",
        boilerplate: `function loadSettings() {
  const raw = storage.getItem("settings");
  return JSON.parse(raw);
}
storage.setItem("settings", "not-json{{");
console.log(loadSettings());
`,
        tests: [
          {
            name: "parse is wrapped in try/catch",
            code: `if (!/try\\s*\\{[\\s\\S]*JSON\\.parse[\\s\\S]*\\}\\s*catch/i.test(code)) {
  throw new Error("Wrap the JSON.parse call in try { … } catch { … }.");
}`,
            hint: 'try { return JSON.parse(raw); } catch { return { theme: "light" }; }',
          },
          {
            name: "corrupt data returns the default",
            code: `const fn = new Function(code + "\\nreturn loadSettings();");
const s = fn();
if (!s || s.theme !== "light") throw new Error("Corrupt data should yield { theme: 'light' }, not a crash.");`,
            hint: "The catch block returns the default object.",
          },
          {
            name: "valid data still parses",
            code: `const fn = new Function(code + '; storage.setItem("settings", JSON.stringify({ theme: "dark" })); return loadSettings();');
const s = fn();
if (s.theme !== "dark") throw new Error("Valid JSON must still load correctly.");`,
            hint: "The happy path keeps working: try parses and returns the stored object.",
          },
        ],
      },
    ],
  },
  {
    file: "js-async-practice.json",
    id: "js-async-practice",
    title: "Asynchronous Practice",
    description:
      "Await in the right order, check response.ok before trusting the body — the two habits that make API code reliable.",
    afterLesson: "js-async",
    minutes: 14,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-ordered-await",
        title: "Await in the Right Order",
        prompt: `\`api.loadUser()\` resolves to \`{ name: "Ada" }\` and \`api.loadGreeting(name)\` resolves to a greeting string. Write \`async function run()\` that awaits the user, then awaits the greeting with the user's name, and logs the greeting (should be \`Hello, Ada\`).

Rules:
- Two \`await\`s — the second needs the first's result.`,
        difficulty: "beginner",
        boilerplate:
          "async function run() {\n  // await user, then greeting, then log\n}\nrun();\n",
        tests: [
          {
            name: "greeting uses the awaited name",
            code: `const logs = [];
const fakeApi = { loadUser: () => Promise.resolve({ name: "Ada" }), loadGreeting: (n) => Promise.resolve("Hello, " + n) };
const fn = new Function("api", "console", code + "\\nreturn run;");`,
            hint: "const user = await api.loadUser(); then api.loadGreeting(user.name).",
          },
          {
            name: "logs Hello, Ada",
            code: `const fn = new Function("api", "console", code + "\\nreturn run();");
await fn({ loadUser: () => Promise.resolve({ name: "Ada" }), loadGreeting: (n) => Promise.resolve("Hello, " + n) }, { log: (m) => { globalThis.__got = m; } });
if (globalThis.__got !== "Hello, Ada") throw new Error("Expected the log 'Hello, Ada'.");`,
            hint: "The awaited greeting must be logged — Hello, Ada.",
          },
          {
            name: "greeting awaited, not a pending promise",
            code: `const fn = new Function("api", "console", code + "\\nreturn run();");
const got = await fn({ loadUser: () => Promise.resolve({ name: "Ada" }), loadGreeting: (n) => Promise.resolve("Hello, " + n) }, { log: (m) => { globalThis.__got2 = m; } });
if (typeof globalThis.__got2 !== "string") {
  throw new Error("You logged a pending Promise — the value must be awaited before logging.");
}`,
            hint: "await the loadGreeting call; only awaited values are strings.",
          },
        ],
      },
      {
        id: "practice-fetch-guard",
        title: "Check response.ok Before Using It",
        prompt: `Write \`async function loadUser()\` that fetches \`https://api.example.com/me\`, throws \`new Error("HTTP " + response.status)\` when \`response.ok\` is false, and otherwise returns the parsed JSON. Then call it and log the user's name (the provided \`fetch\` resolves with a working response).

Rules:
- \`await\` both the fetch and \`.json()\`.
- Guard with \`if (!response.ok)\`.`,
        difficulty: "beginner",
        boilerplate:
          "async function loadUser() {\n  // fetch, check ok, parse, return\n}\nloadUser().then((user) => console.log(user.name));\n",
        tests: [
          {
            name: "ok guard present",
            code: `if (!/if\\s*\\(\\s*!\\s*\\w+\\.ok\\s*\\)/.test(code)) {
  throw new Error("Add the guard: if (!response.ok) { throw … }");
}`,
            hint: 'if (!response.ok) throw new Error("HTTP " + response.status);',
          },
          {
            name: "returns the parsed user",
            code: `const fn = new Function("fetch", code + "\\nreturn loadUser();");
const u = await fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ name: "Ada", role: "learner" }) }));
if (u.name !== "Ada") throw new Error("loadUser() should resolve to the parsed user object.");`,
            hint: "return await response.json(); — the parsed body is the resolved value.",
          },
          {
            name: "throws on failure status",
            code: `const fn = new Function("fetch", code + "\\nreturn loadUser();");
try {
  await fn(() => Promise.resolve({ ok: false, status: 500, json: () => Promise.resolve({}) }));
  throw new Error("NO_THROW");
} catch (err) {
  if (err.message === "NO_THROW") throw new Error("A failing response must throw — your guard didn't fire.");
  if (!/HTTP\\s+500/.test(err.message)) throw new Error("The error message should include 'HTTP ' + the status (500).");
}`,
            hint: "The thrown Error should read 'HTTP 500' for a 500 response.",
          },
        ],
      },
    ],
  },
];

// ── shared stubs (same shapes as the sandbox harness) ──
function buildStubs() {
  const makeEl = (tag = "div") => {
    const e = {
      tagName: tag.toUpperCase(),
      textContent: "",
      className: "",
      value: "",
      children: [],
      listeners: {},
      classList: { add: (...c) => c.forEach((x) => (e._added ??= new Set()).add(x)) },
      addEventListener: (type, fn) => (e.listeners[type] = fn),
      appendChild: (c) => e.children.push(c),
    };
    return e;
  };
  const listEl = makeEl("ul");
  return {
    document: {
      createElement: (t) => makeEl(t),
      querySelector: (sel) => (String(sel).includes("todo-list") ? listEl : makeEl("div")),
      getElementById: () => makeEl("div"),
    },
    button: makeEl("button"),
    display: makeEl("span"),
    storage: (() => {
      const m = new Map();
      return {
        setItem: (k, v) => m.set(String(k), String(v)),
        getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null),
        removeItem: (k) => m.delete(String(k)),
      };
    })(),
    api: {
      loadUser: () => Promise.resolve({ name: "Ada" }),
      loadGreeting: (n) => Promise.resolve("Hello, " + n),
    },
    fetch: () =>
      Promise.resolve({ ok: true, json: async () => ({ name: "Ada", role: "learner" }) }),
  };
}

const REFS = {
  "practice-dom-text-and-class": `const heading = document.getElementById("heading");
const intro = document.getElementById("intro");
heading.textContent = "Pipeline running";
intro.classList.add("is-active");`,
  "practice-dom-create-items": `const todos = ["learn the DOM", "build a list", "render from data"];
const list = document.querySelector("#todo-list");
for (const todo of todos) {
  const li = document.createElement("li");
  li.textContent = todo;
  list.appendChild(li);
}`,
  "practice-dom-counter": `let count = 0;
function bump() {
  count = count + 1;
  display.textContent = count;
}
button.addEventListener("click", bump);
bump();
bump();
console.log(display.textContent);`,
  "practice-storage-roundtrip": `function saveSettings(settings) {
  storage.setItem("settings", JSON.stringify(settings));
}
function loadSettings() {
  const raw = storage.getItem("settings");
  if (raw === null) return { theme: "light" };
  try { return JSON.parse(raw); } catch { return { theme: "light" }; }
}
saveSettings({ theme: "dark", fontSize: 16 });
console.log(loadSettings().theme);`,
  "practice-storage-corrupt-guard": `function loadSettings() {
  const raw = storage.getItem("settings");
  try {
    return JSON.parse(raw);
  } catch {
    return { theme: "light" };
  }
}
storage.setItem("settings", "not-json{{");
console.log(loadSettings());`,
  "practice-ordered-await": `async function run() {
  const user = await api.loadUser();
  const greeting = await api.loadGreeting(user.name);
  console.log(greeting);
}
run();`,
  "practice-fetch-guard": `async function loadUser() {
  const response = await fetch("https://api.example.com/me");
  if (!response.ok) {
    throw new Error("HTTP " + response.status);
  }
  return await response.json();
}
loadUser().then((user) => console.log(user.name));`,
};

const WRONGL = {
  "practice-dom-text-and-class": 'heading.innerText = "Wrong";',
  "practice-dom-create-items": "const list = document.querySelector('#todo-list');",
  "practice-dom-counter": "let count = 0;\nbutton.addEventListener('click', () => {});",
  "practice-storage-roundtrip": 'function saveSettings(s) { storage.setItem("settings", s); }',
  "practice-storage-corrupt-guard":
    "function loadSettings() { return JSON.parse(storage.getItem('settings')); }",
  "practice-ordered-await":
    "async function run() { console.log(api.loadGreeting(api.loadUser().name)); }",
  "practice-fetch-guard":
    "async function loadUser() { const r = await fetch('https://api.example.com/me'); return r; }",
};

function runTest(testCode, studentCode, stubs) {
  const sandbox = {
    code: studentCode,
    result: undefined,
    setTimeout,
    clearTimeout,
    console: { log: () => {}, error: () => {}, warn: () => {} },
    ...stubs,
  };
  const ctx = vm.createContext(sandbox);
  return new vm.Script(
    `(async () => { try { ${testCode}\n result = "PASS"; } catch (err) { result = "FAIL: " + (err && err.message ? err.message : String(err)); } })()`,
  )
    .runInContext(ctx, { awaitPromise: true })
    .then(() => sandbox.result);
}

let appended = 0;
for (const set of SETS) {
  mkdirSync(path.join(BASE, set.id, "challenges"), { recursive: true });
  const setPath = path.join(BASE, set.file);
  if (!existsSync(setPath)) {
    writeFileSync(
      setPath,
      JSON.stringify(
        {
          id: set.id,
          title: set.title,
          description: set.description,
          afterLesson: set.afterLesson,
          minutes: set.minutes,
          difficulty: set.difficulty,
          challenges: set.challenges.map((c) => c.id),
        },
        null,
        2,
      ) + "\n",
    );
  }
  for (const ch of set.challenges) {
    const chPath = path.join(P(set.id), `${ch.id}.json`);
    if (!existsSync(chPath)) {
      writeFileSync(chPath, JSON.stringify(ch, null, 2) + "\n");
    }
    appendFileSync(
      SOLUTIONS_FILE,
      `R[${JSON.stringify(ch.id)}] = ${JSON.stringify(REFS[ch.id])};\nW[${JSON.stringify(ch.id)}] = ${JSON.stringify(WRONGL[ch.id])};\n`,
    );
    appended++;
    // verification with fresh stubs per run
    const stubs1 = buildStubs();
    const stubs2 = buildStubs();
    const results = [];
    for (const t of ch.tests) results.push(await runTest(t.code, REFS[ch.id], stubs1));
    const refOk = results.every((r) => r === "PASS");
    const wrongResults = [];
    for (const t of ch.tests) wrongResults.push(await runTest(t.code, WRONGL[ch.id], stubs2));
    const wrongOk = wrongResults.some((r) => r !== "PASS");
    console.log(
      `${refOk && wrongOk ? "OK " : "FAIL"} ${ch.id} [${results.filter((r) => r === "PASS").length}/${results.length}]`,
    );
    if (!refOk)
      results.forEach((r, i) => {
        if (r !== "PASS") console.log(`   ref [${ch.tests[i].name}]: ${r}`);
      });
    if (!wrongOk) console.log(`   wrong solution passed all tests!`);
  }
}
console.log(`appended ${appended} solution pairs`);
