/**
 * Challenge QA harness: for EVERY challenge in the course, execute its tests
 * in Node (mirroring the sandbox test-file wrapper) against:
 *   1. a per-challenge reference solution  → every test must PASS
 *   2. a per-challenge wrong solution      → at least one test must FAIL
 *
 * This verifies the actual grading behavior end-to-end, not just that JSON parses.
 * Run: node scripts/content-authoring/verify-challenges.mjs
 */
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const TRACK = "src/content/tracks/web-development/courses/web-development-beginner/modules";

/** Mirrors buildTestFile(): author snippet inside try/catch with `code` bound. */
function runTestSnippet(testCode, studentCode, sandboxArgs) {
  const sandbox = {
    code: studentCode,
    console: { log: () => {}, error: () => {}, warn: () => {} },
    result: undefined,
    // REAL timers — async test snippets rely on genuine scheduling.
    setTimeout,
    clearTimeout,
    ...sandboxArgs,
  };
  const context = vm.createContext(sandbox);
  // top-level await support: wrap in an async IIFE
  const script = new vm.Script(
    `(async () => { try { ${testCode}\n result = "PASS"; } catch (err) { result = "FAIL: " + (err && err.message ? err.message : String(err)); } })()`,
  );
  const promise = script.runInContext(context, { awaitPromise: true });
  return promise.then(() => sandbox.result);
}

async function runChallengeTests(challenge, solution, sandboxArgs) {
  const results = [];
  for (const t of challenge.tests) {
    const r = await runTestSnippet(t.code, solution, sandboxArgs);
    results.push({ name: t.name, result: r });
  }
  return results;
}

// ── Per-run stubs: FRESH objects for every execution (tests mutate state). ──
function buildStubs(challengeId) {
  const DOM_CHALLENGES = [
    "click-counter",
    "signup-validator",
    "dom-update-practice",
    "render-a-list",
    "task-tracker-app",
    "persist-a-preference",
    "sequence-with-await",
    "load-and-display-user",
  ];
  if (!DOM_CHALLENGES.includes(challengeId)) return {};

  const makeEl = (tag = "div") => {
    const e = {
      tagName: tag.toUpperCase(),
      textContent: "",
      className: "",
      src: "",
      alt: "",
      value: "",
      children: [],
      listeners: {},
      classList: {
        add: (...c) => c.forEach((x) => e._added.add(x)),
        remove: () => {},
        toggle: () => {},
      },
      _added: new Set(),
      addEventListener: (type, fn) => (e.listeners[type] = fn),
      appendChild: (c) => e.children.push(c),
      remove: () => {},
    };
    return e;
  };
  const listEl = makeEl("ul");
  return {
    api: {
      loadUser: () => Promise.resolve({ name: "Ada" }),
      loadGreeting: (n) => Promise.resolve("Hello, " + n),
    },
    fetch: () =>
      Promise.resolve({
        ok: true,
        json: async () => ({ name: "Ada", role: "learner" }),
      }),
    checkReady: () => Promise.resolve(true),
    storage: (() => {
      const m = new Map();
      return {
        setItem: (k, v) => m.set(String(k), String(v)),
        getItem: (k) => (m.has(String(k)) ? m.get(String(k)) : null),
        removeItem: (k) => m.delete(String(k)),
      };
    })(),
    document: {
      createElement: (t) => makeEl(t),
      querySelector: (sel) =>
        String(sel).includes("task-list") || String(sel).includes("todo-list")
          ? listEl
          : makeEl("div"),
      getElementById: () => listEl,
    },
    button: makeEl("button"),
    display: makeEl("span"),
    heading: makeEl("h1"),
    intro: makeEl("p"),
    hero: makeEl("img"),
    form: makeEl("form"),
    usernameInput: makeEl("input"),
    emailInput: makeEl("input"),
    errorBox: makeEl("div"),
  };
}

// ── Reference solutions, keyed by challenge id ───────────────────────────
const R = {};

// M1 (ported + new) — ids as authored on disk
R["build-a-complete-page"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ada Learns the Web</title>
</head>
<body>
<h1>My Journey Into Web Development</h1>
<p>I started learning how the web works this week.</p>
<p>Next I will build my own pages with confidence.</p>
</body>
</html>`;
R["add-the-missing-link"] = `<!DOCTYPE html>
<html lang="en">
<body>
<a href="https://example.com">Learn more</a>
</body>
</html>`;
R["build-a-recipe-list"] = `<!DOCTYPE html>
<html lang="en">
<body>
<h2>Tomato Soup</h2>
<ul><li>Tomatoes</li><li>Onion</li><li>Basil</li></ul>
<ol><li>Chop</li><li>Cook</li><li>Blend</li></ol>
</body>
</html>`;
R["structure-the-page"] = `<!DOCTYPE html>
<html lang="en">
<body>
<h1>Ada's Bakery</h1>
<header><p>Ada's Bakery</p></header>
<nav><a href="#bread">Bread</a><a href="#cakes">Cakes</a></nav>
<main>
<section><h2 id="bread">Bread</h2><p>Sourdough baked daily.</p></section>
<section><h2 id="cakes">Cakes</h2><p>To order on Fridays.</p></section>
</main>
<footer><p>© 2026 Ada's Bakery</p></footer>
</body>
</html>`;
R["fix-the-heading"] = `<!DOCTYPE html>
<html lang="en">
<body>
<h1>My First Page</h1>
</body>
</html>`;
R["personal-profile-page"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ada Lovelace — Profile</title>
</head>
<body>
<header><h1>Ada Lovelace</h1></header>
<nav>
<a href="#about">About</a>
<a href="#hobbies">Hobbies</a>
<a href="#gallery">Gallery</a>
<a href="#contact">Contact</a>
</nav>
<main>
<section id="about"><h2>About</h2><p>Mathematician and pioneer of computing.</p></section>
<section id="hobbies"><h2>Hobbies</h2><p>Reading, music, and long walks.</p></section>
<section id="gallery"><h2>Gallery</h2><img src="/me.jpg" alt="Portrait of Ada Lovelace at a desk"></section>
<section id="contact"><h2>Contact</h2>
<form>
<label for="email">Email</label>
<input type="email" id="email" name="email">
<button type="submit">Say hello</button>
</form>
</section>
</main>
<footer><p>© 2026 Ada Lovelace</p></footer>
</body>
</html>`;
R["html-understanding-check"] = `<h1>Trattoria Verde</h1>

<img src="https://example.com/pasta.jpg" alt="A bowl of handmade pasta with basil">
<p>Homemade pasta since 1998.</p>

<h2>Our menu</h2>

<ul>
  <li>Tomatoes</li>
  <li>Basil</li>
  <li>Olive oil</li>
</ul>

<a href="https://example.com/menu">View the full menu</a>

<section>
  <h2>Opening hours</h2>
  <ul>
    <li>Mon-Fri: 5pm-10pm</li>
    <li>Sat-Sun: 12pm-11pm</li>
  </ul>
</section>

<button type="button">Book a table</button>`;

// M2 (ported) — form challenges keep the original ids on disk
R["build-a-contact-form"] = `<form>
<label for="email">Email</label>
<input type="email" id="email" name="email" required>
<label for="topic">Topic</label>
<select id="topic" name="topic">
<option>General question</option>
<option>Booking</option>
</select>
<label for="message">Message</label>
<textarea id="message" name="message"></textarea>
<button type="submit">Send message</button>
</form>`;

// M3 — ids as authored on disk
R["style-the-page"] = `<style>
  h1 {
    color: rebeccapurple;
  }

  p {
    font-size: 18px;
  }
</style>`;
R["make-it-readable"] = `<style>
  body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
  }

  h1 {
    font-size: 2rem;
  }

  a {
    color: #0b5fff;
    text-decoration: underline;
  }
</style>`;
R["selector-scavenger-hunt"] = `<style>
  h2 {
    color: #2a6f4e;
  }

  .card {
    background-color: #f7f3ec;
  }

  nav a {
    color: #0b5fff;
  }

  #tagline {
    font-family: Georgia, serif;
  }
</style>`;
R["theme-with-custom-properties"] = `<style>
  :root {
    --brand: #2a6f4e;
    --space: 12px;
  }

  .button {
    background: var(--brand);
    padding: var(--space);
    color: white;
  }

  p {
    font-size: 1rem;
  }
</style>`;
R["box-model-prediction"] = `<style>
  *, *::before, *::after {
    box-sizing: border-box;
  }

  .box {
    width: 200px;
    padding: 20px;
    border: 4px solid dimgray;
    margin: 1rem;
  }
</style>

<div class="box">200 means 200</div>`;
R["space-the-card"] = `<style>
  *, *::before, *::after { box-sizing: border-box; }

  .card {
    width: 400px;
    border: 1px solid silver;
    padding: 1.5rem;
    margin: 0 auto 1.5rem;
    border-radius: 8px;
  }
</style>

<div class="card">
  <h3>Club membership</h3>
  <p>Everything a member needs, one flat rate.</p>
</div>`;
R["display-sorting"] = `<style>
  .badge {
    display: inline-block;
    padding: 2px 8px;
    width: 80px;
  }

  .spacer {
    display: none;
  }

  .para {
    display: block;
  }
</style>`;
R["fix-the-cascade-bug"] = `<style>
  div p {
    color: gray;
  }

  .price {
    color: crimson;
  }
</style>`;
R["flex-the-card-row"] = `<style>
  .row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .card {
    flex: 1;
    min-width: 200px;
  }
</style>`;
R["flex-the-navbar"] = `<style>
  .nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav ul {
    display: flex;
    gap: 1rem;
    list-style: none;
  }

  .nav a {
    color: #0b5fff;
    text-decoration: none;
  }
</style>`;
R["grid-the-gallery"] = `<style>
  .gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .featured {
    grid-column: 1 / -1;
  }
</style>`;
R["badge-the-card"] = `<style>
  .card {
    width: 280px;
    padding: 24px;
    border: 1px solid silver;
    margin: 48px;
    position: relative;
  }

  .badge {
    padding: 2px 8px;
    background: gold;
    position: absolute;
    top: 8px;
    right: 8px;
  }
</style>`;
R["make-it-responsive"] = `<style>
  .cards {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  img {
    max-width: 100%;
    height: auto;
  }

  @media (min-width: 640px) {
    .cards {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (min-width: 1024px) {
    .cards {
      grid-template-columns: repeat(3, 1fr);
    }
  }
</style>`;
R["polish-the-button"] = `<style>
  .button {
    padding: 10px 20px;
    background-color: #4b2e83;
    color: white;
    border: none;
    transition: background-color 0.2s ease;
  }

  .button:hover {
    background-color: #6a44b8;
  }

  .button:focus-visible {
    background-color: #6a44b8;
  }

  @media (prefers-reduced-motion: reduce) {
    .button {
      transition: none;
    }
  }
</style>`;
R["style-the-portfolio"] = `<style>
  *, *::before, *::after { box-sizing: border-box; }

  :root {
    --brand: #2a6f4e;
    --ink: #1c1c1c;
  }

  body {
    font-family: system-ui, sans-serif;
    line-height: 1.6;
    color: var(--ink);
  }

  .site-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  main {
    display: grid;
    gap: 1.5rem;
  }

  .card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    background: var(--brand);
  }

  @media (min-width: 768px) {
    main {
      grid-template-columns: 1fr 1fr;
    }
  }

  a {
    color: var(--brand);
    text-decoration: underline;
    transition: color 0.2s ease;
  }

  @media (prefers-reduced-motion: reduce) {
    a {
      transition: none;
    }
  }
</style>`;

// M4 — JavaScript (refs follow each prompt's own simulation steps exactly)
R["first-console-logs"] = `// greet
console.log("Hello, web!");
console.log("Learning JavaScript today.");`;
R["variables-practice"] =
  'const learner = "Ada";\nlet lessonsDone = 0;\nlessonsDone = 3;\nconst remaining = 15 - lessonsDone;\nconsole.log(`${learner} has ${remaining} lessons left.`);';
// The editor's boilerplate (which the learner keeps) declares price/quantity.
R["types-and-operators"] =
  "const price = 19.99;\nconst quantity = 3;\nconst total = price * quantity;\nconsole.log(`${quantity} items cost ${total}`);\nconsole.log(total > 50);\nconsole.log(total > 10 && total < 100);";
R["grade-classifier"] = `function grade(score) {
  if (score >= 90) return "A";
  else if (score >= 80) return "B";
  else if (score >= 70) return "C";
  return "Keep practicing";
}
console.log(grade(85));
console.log(grade(92));`;
R["countdown-and-sum"] = `function countdown(start) {
  for (let i = start; i >= 1; i--) console.log(i);
}
function sumUpTo(n) {
  let total = 0;
  for (let i = 1; i <= n; i++) total += i;
  return total;
}
console.log(sumUpTo(10));`;
R["temperature-converter"] = `function celsiusToFahrenheit(c) { return c * 9 / 5 + 32; }
console.log(celsiusToFahrenheit(0));
console.log(celsiusToFahrenheit(100));`;
R["function-practice"] = `function greet(name) { return "Hello, " + name + "! Welcome."; }
function maxOfTwo(a, b) { return a >= b ? a : b; }
console.log(greet("Ada"));
console.log(maxOfTwo(7, 3));`;
R["counter-factory"] = `function makeCounter() {
  let count = 0;
  return { increment() { count++; }, value() { return count; } };
}
const counter = makeCounter();
counter.increment();
counter.increment();
console.log(counter.value());`;
R["array-workout"] = `const scores = [45, 92, 67, 88, 30];
const passing = (arr) => arr.filter((s) => s >= 60);
const toPercent = (arr) => arr.map((s) => s * 2);
console.log(passing(scores).length);
console.log(scores.includes(100));`;
R["model-a-learner"] = `const learner = { name: "Ada", streak: 12, skills: ["HTML", "CSS"] };
const isOnFire = (person) => person.streak >= 7;
const cohort = [{ name: "Ada", streak: 12, skills: ["HTML"] }, { name: "Grace", streak: 3, skills: ["JS"] }];
console.log(cohort[1].name);`;
R["dom-update-practice"] = `heading.textContent = "Pipeline running";
intro.classList.add("is-active");
hero.src = "/photos/dawn.jpg";
hero.alt = "Sunrise over a mountain lake";`;
R["render-a-list"] = `const todos = ["learn the DOM", "build a list", "render from data"];
const list = document.querySelector("#todo-list");
for (const todo of todos) {
  const li = document.createElement("li");
  li.textContent = todo;
  list.appendChild(li);
}`;
R["click-counter"] = `let count = 0;
function bump() {
  count = count + 1;
  display.textContent = count;
}
button.addEventListener("click", bump);
// Simulate the two clicks from step 2 by calling the handler logic twice:
bump();
bump();
console.log(display.textContent);`;
R["signup-validator"] = `function handleSubmit(event) {
  event.preventDefault();
  const username = usernameInput.value.trim();
  const email = emailInput.value;
  if (username.length < 3) { errorBox.textContent = "Username must be at least 3 characters."; return; }
  if (!email.includes("@")) { errorBox.textContent = "Please enter a valid email address."; return; }
  errorBox.textContent = "";
  console.log("Welcome, " + username);
}
form.addEventListener("submit", handleSubmit);
// Simulate the three submissions from the prompt:
usernameInput.value = "  ab  "; emailInput.value = "a@b.co";
form.listeners.submit({ preventDefault() {} });
usernameInput.value = "ada"; emailInput.value = "not-an-email";
form.listeners.submit({ preventDefault() {} });
usernameInput.value = "ada"; emailInput.value = "ada@example.com";
form.listeners.submit({ preventDefault() {} });`;
R["persist-a-preference"] =
  `function saveSettings(settings) { storage.setItem("settings", JSON.stringify(settings)); }
function loadSettings() {
  const raw = storage.getItem("settings");
  if (raw === null) return { theme: "light" };
  try { return JSON.parse(raw); } catch { return { theme: "light" }; }
}
saveSettings({ theme: "dark", fontSize: 16 });
console.log(loadSettings().theme);`;
R["sequence-with-await"] = `async function run() {
  const user = await api.loadUser();
  const greeting = await api.loadGreeting(user.name);
  console.log(greeting);
}
run();`;
R["load-and-display-user"] = `async function loadUser() {
  const response = await fetch("https://api.example.com/me");
  if (!response.ok) throw new Error("HTTP " + response.status);
  return await response.json();
}
loadUser().then((user) => console.log(user.name));`;
R["js-fundamentals-checkpoint"] = `function average(numbers) {
  if (numbers.length === 0) return 0;
  let total = 0;
  for (const n of numbers) total += n;
  return total / numbers.length;
}
function formatScore(name, score) { return name + " scored " + score; }
function bestLearner(learners) {
  let best = learners[0];
  for (const l of learners) if (l.score > best.score) best = l;
  return best;
}
async function announce() { const ok = await checkReady(); return ok ? "ready" : "not ready"; }`;
R["task-tracker-app"] = `const tasks = JSON.parse(storage.getItem("tasks")) ?? [];
const list = document.querySelector("#task-list");
function save() { storage.setItem("tasks", JSON.stringify(tasks)); }
function render() {
  list.children.length = 0;
  for (const t of tasks) {
    const li = document.createElement("li");
    li.textContent = (t.done ? "[x] " : "[ ] ") + t.title;
    list.appendChild(li);
  }
}
function addTask(title) { tasks.push({ title, done: false }); save(); render(); }
function toggleTask(index) { tasks[index].done = !tasks[index].done; save(); render(); }
addTask("learn state");
addTask("build tracker");
toggleTask(0);`;

// M5/M6/M7 (knowledge checks — answers ARE the solution)
R["terminal-commands"] =
  `const answers = { where: "pwd", list: "ls", enter: "cd my-project", up: "cd ..", makeFolder: "mkdir notes" };`;
R["git-init-and-commit"] = `function commitSequence() {
  return ["git init", "git status", "git add .", 'git commit -m "First page"'];
}`;
R["branch-workflow"] = `const branchWorkflow = () => ({
  create: "git branch feature/faq",
  switch: "git switch feature/faq",
  merge: "git merge feature/faq",
});`;
R["push-to-github"] = `function publishCommands() {
  return [
    "git remote add origin https://github.com/ada/my-site.git",
    "git push -u origin main",
    "git clone https://github.com/ada/my-site.git",
  ];
}`;
R["deploy-checklist"] = `const fix = () => ({
  problem: "paths",
  fix: '<link rel="stylesheet" href="./styles.css">',
});`;
R["workflow-checkpoint"] =
  `const answers = { undoTarget: "revert", safeShare: "pull request", stage: "add" };`;
R["architecture-sort"] =
  `const answers = { passwordCheck: "backend", buttonText: "frontend", priceCalculation: "backend", themeToggle: "frontend", databaseQuery: "backend" };`;
R["http-status-code-check"] =
  `const answers = { anonymousRun: 401, missingPage: 404, tooManyRequests: 429, allGood: 200 };`;
R["capstone-verification"] = `const capstone = {
  layout: "both",
  nav: "hamburger",
  storageKey: "tasks",
  contrastChecked: true,
  keyboardNavigable: true,
  formLabeled: true,
};`;

// Wrong solutions: must fail ≥1 test. Default: empty solution fails everything.
const WRONG_DEFAULT = "";
const W = {
  // a plausible-but-wrong attempt per structural HTML/CSS challenge
  ...Object.fromEntries(
    [
      "build-a-complete-page",
      "add-the-missing-link",
      "semantic-page",
      "accessible-image",
      "build-a-list",
      "build-a-contact-form",
      "personal-profile-page",
      "html-understanding-check",
      "portfolio-page",
    ].map((id) => [id, "<html><body>nothing here</body></html>"]),
  ),
  ...Object.fromEntries(
    [
      "style-the-page",
      "make-it-readable",
      "selector-scavenger-hunt",
      "theme-with-custom-properties",
      "box-model-prediction",
      "space-the-card",
      "display-sorting",
      "fix-the-cascade-bug",
      "flex-the-card-row",
      "flex-the-navbar",
      "grid-the-gallery",
      "badge-the-card",
      "make-it-responsive",
      "polish-the-button",
      "style-the-portfolio",
      "css-understanding-check",
      "specificity-showdown",
      "typography-makeover",
      "box-model-practice",
      "cascade-debug",
      "layout-flexbox",
      "layout-grid",
      "responsive-page",
      "motion-with-focus",
    ].map((id) => [id, "/* wrong: */ p { color: red; }"]),
  ),
  "first-console-logs": 'console.log("hi");',
  "variables-practice": 'let learner = "Ada";',
  "types-and-operators": "const total = 60;",
  "grade-classifier": 'function grade(score) { return "A"; }',
  "countdown-and-sum": "function sumUpTo(n) { return 55; }",
  "counter-factory": "function makeCounter() { return {}; }",
  "array-workout": "const passing = (a) => a;",
  "model-a-learner": "const learner = { name: 5 };",
  "dom-update-practice": "heading.textContent = 'Wrong';",
  "render-a-list": "const list = document.querySelector('#todo-list');",
  "click-counter": "let count = 0;",
  "signup-validator": "form.addEventListener('submit', () => {});",
  "persist-a-preference": 'function saveSettings(s) { storage.setItem("settings", s); }',
  "sequence-with-await": "async function run() { console.log(api.loadUser()); }",
  "load-and-display-user": "async function loadUser() { return { name: 'Ada' }; }",
  "js-fundamentals-checkpoint": "function average(n) { return 0; }",
  "task-tracker-app": "const tasks = [];",
  "terminal-commands":
    'const answers = { where: "", list: "", enter: "", up: "", makeFolder: "" };',
  "git-init-and-commit": "function commitSequence() { return []; }",
  "branch-workflow": "const branchWorkflow = () => ({});",
  "push-to-github": "function publishCommands() { return []; }",
  "deploy-checklist": "const fix = () => ({ problem: 'case', fix: '' });",
  "workflow-checkpoint":
    'const answers = { undoTarget: "log", safeShare: "push", stage: "commit" };',
  "architecture-sort":
    'const answers = { passwordCheck: "frontend", buttonText: "frontend", priceCalculation: "frontend", themeToggle: "frontend", databaseQuery: "frontend" };',
  "http-status-code-check":
    "const answers = { anonymousRun: 400, missingPage: 400, tooManyRequests: 500, allGood: 201 };",
  "capstone-verification":
    'const capstone = { layout: "", nav: "", storageKey: "", contrastChecked: false, keyboardNavigable: false, formLabeled: false };',
};

let passCount = 0;
let failCount = 0;
const failures = [];

const modules = readdirSync(TRACK);
for (const mod of modules) {
  const lessonsDir = path.join(TRACK, mod, "lessons");
  const entries = readdirSync(lessonsDir);
  for (const entry of entries) {
    if (!entry.endsWith(".json")) continue;
    const lesson = JSON.parse(readFileSync(path.join(lessonsDir, entry), "utf8"));
    const chDir = path.join(lessonsDir, lesson.id, "challenges");
    let challengeFiles = [];
    try {
      challengeFiles = readdirSync(chDir).filter((f) => f.endsWith(".json"));
    } catch {
      continue; // no challenges dir
    }
    for (const cf of challengeFiles) {
      const challenge = JSON.parse(readFileSync(path.join(chDir, cf), "utf8"));
      const ref = R[challenge.id] ?? R[cf.replace(".json", "")];
      const wrong = W[challenge.id] ?? WRONG_DEFAULT;
      if (ref === undefined) {
        failCount++;
        failures.push(challenge.id);
        console.log(`  FAIL ${challenge.id} — no reference solution in harness`);
        continue;
      }

      // 1. reference solution must pass every test (fresh stubs)
      const refResults = await runChallengeTests(challenge, ref, buildStubs(challenge.id));
      const refOk = refResults.every((r) => r.result === "PASS");
      // 2. wrong solution must fail at least one test (fresh stubs)
      const wrongResults = await runChallengeTests(challenge, wrong, buildStubs(challenge.id));
      const wrongOk = wrongResults.some((r) => r.result !== "PASS");

      if (refOk && wrongOk) {
        passCount++;
        console.log(`  OK  ${challenge.id}`);
      } else {
        failCount++;
        console.log(`  FAIL ${challenge.id} (refOk=${refOk} wrongOk=${wrongOk})`);
        for (const r of refResults) {
          if (r.result !== "PASS") console.log(`    ref failed [${r.name}]: ${r.result}`);
        }
        if (!wrongOk) {
          for (const r of wrongResults) console.log(`    wrong passed [${r.name}]`);
        }
        failures.push(challenge.id);
      }
    }
  }
}

console.log(`\n${passCount} challenges verified, ${failCount} failed`);
if (failures.length) {
  console.log("FAILURES:", failures.join(", "));
  process.exit(1);
}
