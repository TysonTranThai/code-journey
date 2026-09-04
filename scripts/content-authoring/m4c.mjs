/**
 * Author Module 4 (JavaScript Foundations) — script C: lessons 10–13.
 * DOM selection/modification, creating elements, events, forms & validation.
 *
 * Escaping-safe convention: NO raw backticks and NO raw "${" in content.
 * Backticks from T, dollars from D; code fences use ~~~.
 * DOM challenges grade behavior against stub objects — no implementation lock-in.
 *
 * Run: node scripts/content-authoring/m4c.mjs
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

/* ── 4.10 The DOM: selecting & changing ─────────────────────────────── */

writeLesson(
  "js-dom-select",
  "The DOM: Reading and Changing the Page",
  "The DOM is your page as a live object tree. Select elements and change their text, attributes, and styles from JavaScript.",
  16,
  "intermediate",
  ["dom-update-practice"],
  `
The browser reads your HTML and builds the **DOM** (Document Object Model) — a live
tree of objects, one per element. Change an object, and the page updates instantly.

## document — the entry point

~~~js
// by id (fastest, most precise) — ONE element or null
const title = document.getElementById("page-title");

// by CSS selector — first match / all matches
const firstCard = document.querySelector(".card");
const allCards  = document.querySelectorAll(".card");   // a NodeList (array-like)
~~~

${T}querySelector${T}/${T}querySelectorAll${T} take any CSS selector you already
know: ${T}"#save-btn"${T}, ${T}".nav-link"${T}, ${T}"form input[type=email]"${T}.

## Changing text

~~~js
title.textContent = "My new heading";
~~~

${T}textContent${T} sets the element's text safely. (You may also see
${T}innerHTML${T} — it parses HTML and can run injected code; avoid it for text.)

## Changing attributes

~~~js
const img = document.querySelector("img");
img.src = "/new-photo.jpg";
img.alt = "A mountain lake at dawn";
const link = document.querySelector("a");
link.href = "https://developer.mozilla.org";
link.target = "_blank";
~~~

Element objects have a property per HTML attribute — read them too:
${T}img.src${T} returns the current value.

## Changing styles and classes

~~~js
const box = document.querySelector(".box");
box.style.color = "crimson";          // inline style (camelCase properties)
box.classList.add("is-open");         // the better way: toggle CSS classes
box.classList.remove("hidden");
box.classList.toggle("dark");         // adds if missing, removes if present
~~~

Prefer ${T}classList${T} over ${T}style${T} — put the appearance in CSS where it
belongs, and let JavaScript only flip the switch.

## The null check habit

${T}querySelector${T} returns ${T}null${T} when nothing matches. Then
${T}title.textContent = ...${T} throws ${T}TypeError: null${T} — check what you
actually selected:

~~~js
const btn = document.querySelector("#save");
if (btn) {
  btn.textContent = "Saving…";
}
~~~

## What you learned

- The DOM is the page as a live object tree; ${T}document${T} is the entry point
- ${T}getElementById${T}, ${T}querySelector${T}, ${T}querySelectorAll${T}
- ${T}textContent${T}, attribute properties, ${T}style${T}, and ${T}classList${T}
- Missing elements return ${T}null${T} — check before you set

**Next:** creating brand-new elements, not just editing existing ones.
`,
);

writeChallenge("js-dom-select", {
  id: "dom-update-practice",
  title: "Update the Page",
  prompt:
    "A page is loaded for you: a heading with id \"status\", a paragraph with class \"intro\", and an image with id \"hero\". JavaScript received the real element objects as `heading`, `intro`, and `hero` — do NOT call document.querySelector; use these variables directly.\n\n1. Set the heading's text to exactly: Pipeline running\n2. Add the class \"is-active\" to the intro paragraph.\n3. Set the hero image's src to \"/photos/dawn.jpg\" and give its alt text a meaningful description.",
  difficulty: "intermediate",
  boilerplate: "// heading, intro, hero are the real element objects\n\n// 1) heading text\n\n// 2) intro class\n\n// 3) hero image\n",
  tests: [
    {
      name: "heading text set to Pipeline running",
      code: `function el() { return { classList: { add() {}, remove() {}, toggle() {} } }; }
const heading = el(), intro = el(), hero = el();
new Function("heading", "intro", "hero", code)(heading, intro, hero);
if (heading.textContent !== "Pipeline running") {
  throw new Error('heading.textContent should be exactly "Pipeline running" — got "' + heading.textContent + '".');
}`,
      hint: "heading.textContent = \"Pipeline running\";",
    },
    {
      name: "intro gets is-active via classList.add",
      code: `const added = [];
function el() { return { classList: { add: (c) => added.push(c), remove() {}, toggle() {} } }; }
const heading = el(), intro = el(), hero = el();
new Function("heading", "intro", "hero", code)(heading, intro, hero);
if (!added.includes("is-active")) {
  throw new Error('Call intro.classList.add("is-active").');
}`,
      hint: 'intro.classList.add("is-active");',
    },
    {
      name: "hero src and alt set",
      code: `function el() { return { classList: { add() {}, remove() {}, toggle() {} } }; }
const heading = el(), intro = el(), hero = el();
new Function("heading", "intro", "hero", code)(heading, intro, hero);
if (hero.src !== "/photos/dawn.jpg") {
  throw new Error('Set hero.src to "/photos/dawn.jpg".');
}
if (typeof hero.alt !== "string" || hero.alt.length < 8) {
  throw new Error("Give the image a meaningful alt description (at least a few words).");
}`,
      hint: 'hero.src = "/photos/dawn.jpg"; hero.alt = "Sunrise over a mountain lake";',
    },
  ],
});

/* ── 4.11 Creating & removing elements ──────────────────────────────── */

writeLesson(
  "js-dom-create",
  "Creating and Removing Elements",
  "Build new DOM nodes from data and attach them to the page — how lists, cards, and entire views are rendered.",
  14,
  "intermediate",
  ["render-a-list"],
  `
Editing existing elements is half the story. The other half is **creating** them —
that is how a feed, a search results list, or a cart comes to exist at all.

## The recipe: create → fill → attach

~~~js
const li = document.createElement("li");     // 1. create (not on the page yet)
li.textContent = "Learn the DOM";            // 2. fill it
list.appendChild(li);                        // 3. attach to a parent
~~~

A new element floats unattached until you append it — ${T}appendChild${T} is the
moment it appears.

## Building structured content

Elements nest the same way they do in HTML:

~~~js
const card = document.createElement("article");
card.className = "card";            // className sets the class attribute

const h3 = document.createElement("h3");
h3.textContent = "Ada Lovelace";

const p = document.createElement("p");
p.textContent = "Wrote the first algorithm.";

card.appendChild(h3);
card.appendChild(p);
feed.appendChild(card);
~~~

## Rendering from data — the pattern that runs the web

~~~js
const skills = ["HTML", "CSS", "JavaScript"];
const list = document.querySelector("#skills");

for (const skill of skills) {
  const li = document.createElement("li");
  li.textContent = skill;
  list.appendChild(li);
}
~~~

The data lives in the array; the DOM is just its projection. Change the array,
re-render, and the page follows. Every framework you will ever learn is a shortcut
around this loop.

## for...of — looping without an index

${T}for (const item of items)${T} visits each value in turn — perfect when you do
not need the index.

## Removing

~~~js
item.remove();          // the element removes itself
~~~

## Accessibility note

Screen readers follow the DOM, so structure matters even when JavaScript builds it:
use real list elements for lists, headings in order, and the same semantic elements
you would have written by hand.

## What you learned

- ${T}createElement${T} → fill → ${T}appendChild${T}
- ${T}className${T} sets classes on new elements
- Render-from-data: loop the array, build one element per item
- ${T}for...of${T} visits values without an index; ${T}.remove()${T} deletes

**Next:** making the page respond to people — events.
`,
);

writeChallenge("js-dom-create", {
  id: "render-a-list",
  title: "Render a List from Data",
  prompt:
    "The `document` object in this challenge records what you build — use it exactly like the real one: document.createElement(tag), document.querySelector(selector), and parent.appendChild(child).\n\n1. Select the list with id \"todo-list\".\n2. Loop over the given `todos` array (it is provided in the boilerplate) and for each item: create an <li>, set its text to the todo, and append it to the list.",
  difficulty: "intermediate",
  boilerplate:
    'const todos = ["learn the DOM", "build a list", "render from data"];\n\n// 1) select #todo-list\n\n// 2) create + fill + append one <li> per todo\n',
  tests: [
    {
      name: "three list items appended",
      code: `function makeDoc() {
  const elements = [];
  const byId = {};
  function make(tag) {
    const e = { tagName: String(tag).toUpperCase(), textContent: "", className: "", children: [], parent: null };
    e.appendChild = (c) => { c.parent = e; e.children.push(c); };
    e.remove = () => {};
    elements.push(e);
    return e;
  }
  const list = make("ul");
  byId["todo-list"] = list;
  return {
    elements,
    doc: {
      createElement: (t) => make(t),
      querySelector: (sel) => (String(sel).includes("todo-list") ? list : null),
      getElementById: (id) => byId[id] ?? null,
    },
    list,
  };
}
const { elements, doc, list } = makeDoc();
new Function("document", code + ";return undefined;")(doc);
const lis = list.children.filter((c) => c.tagName === "LI");
if (lis.length !== 3) {
  throw new Error("Expected 3 <li> elements appended — got " + lis.length + ". Create one per todo and append it.");
}`,
      hint: "for (const todo of todos) { const li = document.createElement(\"li\"); li.textContent = todo; list.appendChild(li); }",
    },
    {
      name: "items contain the right text, in order",
      code: `function makeDoc() {
  function make(tag) {
    const e = { tagName: String(tag).toUpperCase(), textContent: "", className: "", children: [], parent: null };
    e.appendChild = (c) => { c.parent = e; e.children.push(c); };
    e.remove = () => {};
    return e;
  }
  const list = make("ul");
  return { doc: { createElement: (t) => make(t), querySelector: () => list, getElementById: () => list }, list };
}
const { doc, list } = makeDoc();
new Function("document", code + ";return undefined;")(doc);
const texts = list.children.filter((c) => c.tagName === "LI").map((c) => c.textContent);
const want = ["learn the DOM", "build a list", "render from data"];
if (JSON.stringify(texts) !== JSON.stringify(want)) {
  throw new Error("The list items should carry the todo texts in order — got " + JSON.stringify(texts) + ".");
}`,
      hint: "Set li.textContent = todo (the loop variable) — not a fixed string.",
    },
  ],
});

/* ── 4.12 Events ─────────────────────────────────────────────────────── */

writeLesson(
  "js-dom-events",
  "Events: Listening and Reacting",
  "Code that waits: addEventListener connects user actions — clicks, typing, submits — to your functions.",
  16,
  "intermediate",
  ["click-counter"],
  `
So far your code has run top to bottom, once. **Events** change everything: you
register a function, and the browser calls it whenever the action happens — a click,
a keypress, a form submit.

## addEventListener

~~~js
const btn = document.querySelector("#save");

btn.addEventListener("click", () => {
  console.log("Clicked!");
});
~~~

Read it as: *on ${T}btn${T}, whenever a ${T}click${T} happens, run this function.*
The function is the **handler** — the browser calls it, not you. Nothing happens
until the user acts.

## The common events

| Event | Fires when |
|---|---|
| ${T}click${T} | an element is clicked or tapped |
| ${T}input${T} | a text field's value changes, per keystroke |
| ${T}submit${T} | a form is submitted (on the **form**, not the button) |
| ${T}keydown${T} | a key is pressed |

~~~js
const field = document.querySelector("#search");
field.addEventListener("input", () => {
  console.log("Now contains:", field.value);
});
~~~

## The event object and preventDefault

Handlers receive an **event object** with details of what happened:

~~~js
const form = document.querySelector("#signup");

form.addEventListener("submit", (event) => {
  event.preventDefault();        // stop the browser's full-page reload
  console.log("Handling the submit ourselves");
});
~~~

${T}event.preventDefault()${T} cancels the default browser behavior. For forms that
is essential: without it, submitting reloads the page and your JavaScript never gets
to respond. Nearly every modern app intercepts submit this way and updates the page
in place.

## Buttons: click handlers with real work

~~~js
const counterBtn = document.querySelector("#increment");
const display = document.querySelector("#count");
let count = 0;

counterBtn.addEventListener("click", () => {
  count++;                       // update state first…
  display.textContent = count;   // …then reflect it in the page
});
~~~

State first, render second — this two-step dance is the core of every interactive
app you will build.

## What you learned

- ${T}element.addEventListener("click", handler)${T} — the browser calls your function
- ${T}click${T}, ${T}input${T}, ${T}submit${T}, ${T}keydown${T}
- Handlers receive an event object; ${T}preventDefault()${T} stops default behavior
- Update state, then render it

**Next:** forms — collecting and validating user input.
`,
);

writeChallenge("js-dom-events", {
  id: "click-counter",
  title: "Build a Click Counter",
  prompt:
    "Elements `button` (a \"increment\" button) and `display` (shows the count) are provided as variables.\n\n1. Add a click listener to `button` that increases `count` (starting at 0) and updates `display.textContent` with the new count.\n2. To prove it works, simulate two clicks by CALLING the handler logic twice, then log `display.textContent` — it should print 2.\n\nTip: keep the handler in a variable or use a named function so you can call it yourself.",
  difficulty: "intermediate",
  boilerplate: "let count = 0;\n\n// 1) wire button's click listener to update count + display\n\n// 2) trigger it twice, then log display.textContent\n",
  tests: [
    {
      name: "a click listener is registered",
      code: `function makeEl() {
  return {
    listeners: {},
    addEventListener(type, fn) { this.listeners[type] = fn; },
    textContent: "",
    dispatch(type) { if (this.listeners[type]) this.listeners[type]({ preventDefault() {} }); },
  };
}
const button = makeEl(), display = makeEl();
new Function("button", "display", code)(button, display);
if (typeof button.listeners.click !== "function") {
  throw new Error("Register a click handler: button.addEventListener(\"click\", ...)");
}`,
      hint: "button.addEventListener(\"click\", () => { count++; display.textContent = count; });",
    },
    {
      name: "two clicks lead to display showing 2",
      code: `function makeEl() {
  return {
    listeners: {},
    addEventListener(type, fn) { this.listeners[type] = fn; },
    textContent: "",
    dispatch(type) { if (this.listeners[type]) this.listeners[type]({ preventDefault() {} }); },
  };
}
const button = makeEl(), display = makeEl();
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("button", "display", "console", code)(button, display, fakeConsole);
if (display.textContent !== "2") {
  throw new Error('After two clicks, display.textContent should be "2" — got "' + display.textContent + '". Update state, then render it.');
}`,
      hint: "Count in the outer `count` variable; set display.textContent = count inside the handler; call the handler twice.",
    },
    {
      name: "the count was logged",
      code: `function makeEl() {
  return {
    listeners: {},
    addEventListener(type, fn) { this.listeners[type] = fn; },
    textContent: "",
    dispatch(type) { if (this.listeners[type]) this.listeners[type]({ preventDefault() {} }); },
  };
}
const button = makeEl(), display = makeEl();
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("button", "display", "console", code)(button, display, fakeConsole);
if (!logs.some((l) => l === "2")) {
  throw new Error("Log display.textContent after the two simulated clicks — the console should show 2.");
}`,
      hint: "console.log(display.textContent); after triggering the handler twice.",
    },
  ],
});

/* ── 4.13 Forms & validation ─────────────────────────────────────────── */

writeLesson(
  "js-forms-and-validation",
  "Forms: Reading Input and Validating",
  "Get data out of a form, check it before trusting it, and give the user clear feedback — both browser-native and JavaScript-side.",
  16,
  "intermediate",
  ["signup-validator"],
  `
Forms are how your site *listens*. You know the HTML (Module 2) and events (last
lesson) — now you read what the user typed and check it.

## Reading values

~~~js
const emailField = document.querySelector("#email");

emailField.value        // the current text — a string, always
~~~

${T}.value${T} works on inputs, textareas, and selects. It is **always a string**:
${T}"25"${T} is not a number — convert with ${T}Number(...)${T} when you do math.

## Two layers of validation

**Layer 1 — the browser (free):** with
${T}<input type="email" required minlength="3">${T}, the browser refuses to submit
invalid data and shows a message. Always start here.

**Layer 2 — your JavaScript:** the browser can't know your business rules ("name
taken", "username must not contain spaces"). Handle the submit and check yourself:

~~~js
const form = document.querySelector("#signup");
const errorBox = document.querySelector("#error");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const username = document.querySelector("#username").value.trim();

  if (username.length < 3) {
    errorBox.textContent = "Username must be at least 3 characters.";
    return;                       // stop — don't accept the bad input
  }

  errorBox.textContent = "";      // clear old errors
  console.log("Welcome, " + username);
});
~~~

## Feedback that includes everyone

- Show errors in **text on the page** (color alone fails ~8% of men — colorblind
  users can't see "the red border").
- Put the message near the field it belongs to.
- ${T}.trim()${T} before checking: "  " is not a real name even though it is not
  empty.

## The pattern, generalized

1. Intercept submit → ${T}preventDefault()${T}
2. Read + normalize values
3. Check each rule; on first failure, show a message and stop
4. All good → do the real work (save, send, render)

This read → validate → feedback loop is unchanged in every framework.

## What you learned

- ${T}.value${T} reads fields; it is always a string (${T}Number()${T} to convert)
- Validate in layers: HTML attributes first, JavaScript for your rules
- Show errors as text near the field; never color alone
- Intercept, read, check, feedback — in that order

**Next:** remembering data between visits — storage.
`,
);

writeChallenge("js-dom-events", {
  id: "signup-validator",
  title: "Validate a Signup Form",
  prompt:
    "Elements are provided: `form`, `usernameInput` (a text field), `emailInput`, and `errorBox`. Build the submit flow:\n\n1. Add a submit listener to `form` that calls event.preventDefault() first.\n2. Read the username; if its trimmed length is under 3, set `errorBox.textContent` to a helpful message and stop.\n3. Read the email; if it does not include \"@\", show an error the same way.\n4. Otherwise clear `errorBox.textContent` and log `Welcome, <username>`.\n\nThen simulate: submit with username \"ab\" (too short), then submit with a valid username and email — and log after each.",
  difficulty: "intermediate",
  boilerplate:
    "// form, usernameInput, emailInput, errorBox are provided element objects\n\n// wire the submit listener with validation\n\n// simulate the two submissions\n",
  tests: [
    {
      name: "submit listener registered and default prevented",
      code: `function makeEl(extra = {}) {
  return {
    listeners: {},
    value: "",
    textContent: "",
    addEventListener(type, fn) { this.listeners[type] = fn; },
    dispatch(type) {
      const prevented = { flag: false };
      if (this.listeners[type]) this.listeners[type]({ preventDefault() { prevented.flag = true; } });
      return prevented;
    },
    ...extra,
  };
}
const form = makeEl(), usernameInput = makeEl({ value: "ab" }), emailInput = makeEl({ value: "a@b.co" }), errorBox = makeEl();
new Function("form", "usernameInput", "emailInput", "errorBox", code)(form, usernameInput, emailInput, errorBox);
if (typeof form.listeners.submit !== "function") {
  throw new Error("Register a submit handler on the form.");
}
const prevented = form.dispatch("submit");
if (!prevented.flag) {
  throw new Error("Call event.preventDefault() inside the submit handler.");
}`,
      hint: "form.addEventListener(\"submit\", (event) => { event.preventDefault(); ... });",
    },
    {
      name: "short username shows an error and stops",
      code: `function makeEl(extra = {}) {
  return {
    listeners: {},
    value: "",
    textContent: "",
    addEventListener(type, fn) { this.listeners[type] = fn; },
    dispatch(type) {
      const prevented = { flag: false };
      if (this.listeners[type]) this.listeners[type]({ preventDefault() { prevented.flag = true; } });
      return prevented;
    },
    ...extra,
  };
}
const form = makeEl(), usernameInput = makeEl({ value: "  ab  " }), emailInput = makeEl({ value: "a@b.co" }), errorBox = makeEl();
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("form", "usernameInput", "emailInput", "errorBox", "console", code)(form, usernameInput, emailInput, errorBox, fakeConsole);
if (!errorBox.textContent || errorBox.textContent.length < 5) {
  throw new Error("A too-short username should put a helpful message in errorBox.textContent.");
}
if (logs.some((l) => l.startsWith("Welcome"))) {
  throw new Error("Invalid input must stop the flow — no Welcome log for a 2-character username.");
}`,
      hint: "const username = usernameInput.value.trim(); if (username.length < 3) { errorBox.textContent = \"...\"; return; }",
    },
    {
      name: "valid input clears errors and welcomes",
      code: `function makeEl(extra = {}) {
  return {
    listeners: {},
    value: "",
    textContent: "",
    addEventListener(type, fn) { this.listeners[type] = fn; },
    dispatch(type) {
      const prevented = { flag: false };
      if (this.listeners[type]) this.listeners[type]({ preventDefault() { prevented.flag = true; } });
      return prevented;
    },
    ...extra,
  };
}
const form = makeEl(), usernameInput = makeEl({ value: "ada" }), emailInput = makeEl({ value: "ada@example.com" }), errorBox = makeEl();
const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("form", "usernameInput", "emailInput", "errorBox", "console", code)(form, usernameInput, emailInput, errorBox, fakeConsole);
if (errorBox.textContent !== "") {
  throw new Error("Valid input should clear errorBox.textContent.");
}
if (!logs.some((l) => l === "Welcome, ada")) {
  throw new Error('Log "Welcome, " + username for valid input — expected "Welcome, ada".');
}`,
      hint: "errorBox.textContent = \"\"; console.log(\"Welcome, \" + username);",
    },
  ],
});
