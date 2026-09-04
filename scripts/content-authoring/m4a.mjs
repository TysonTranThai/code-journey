/**
 * Author Module 4 (JavaScript Foundations) — script A: lessons 1–5.
 *
 * Escaping-safe convention: content strings contain NO raw backticks and NO
 * raw "${" sequences. Backticks come from T, dollar signs from D; code fences
 * use ~~~ (valid CommonMark, rendered identically in MDX).
 *
 * Run: node scripts/content-authoring/m4a.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const T = String.fromCharCode(96); // backtick
const D = String.fromCharCode(36); // dollar sign
const F = T + T + T; // code fence (rendered as a Markdown fence via ~~~? no — we use tildes)
void F;

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

/* ── 4.1 What JavaScript Does ────────────────────────────────────────── */

writeLesson(
  "what-javascript-does",
  "What JavaScript Does",
  "The browser's programming language: what it can do, where it runs, and how to see it run with console.log — your first window into every program you will ever write.",
  10,
  "beginner",
  ["first-console-logs"],
  `
HTML is content, CSS is appearance. **JavaScript is behavior** — the only programming
language browsers run natively. Every interactive thing on the web — autocomplete,
drag-and-drop, live scores, form validation — is JavaScript changing the page after
it loads.

## Where it runs

A browser downloads your ${T}.js${T} file and executes it, top to bottom, inside the
page. The same language also runs on servers (Node.js) — that is how Code Journey
grades your challenges — but in this module the browser is home.

## Your first command: console.log

${T}${T}${T}js
console.log("Hello, web!");
${T}${T}${T}

${T}console.log(...)

prints values to the **console** — a panel built into every browser (open it with
F12 or right-click → Inspect → Console). Programmers live in the console: it is
where you check what your code actually did. In these challenges the grader reads
your console output, so ${T}console.log${T} is how your code talks to the tests.

## Statements end with semicolons (usually)

A **statement** is one instruction. Style guides differ, but these challenges expect
a semicolon at the end of each statement:

${T}${T}${T}js
console.log("one");
console.log("two");
${T}${T}${T}

## Comments

Text after ${T}//${T} is ignored by the browser — notes for humans:

${T}${T}${T}js
// greet the learner
console.log("Welcome!");
${T}${T}${T}

## Errors are normal

Type ${T}consolelo.g("x")${T} and the console shows a red **error** with a line
number. Errors are not failure — they are the browser telling you exactly where to
look. Every professional reads errors dozens of times a day.

## What you learned

- JavaScript = behavior; it runs in the browser after the page loads
- ${T}console.log${T} prints values; the console is your feedback loop
- Statements are separated with semicolons; ${T}//${T} starts a comment
- Errors point at the problem — read them

**Next:** storing values with variables.
`,
);

writeChallenge("what-javascript-does", {
  id: "first-console-logs",
  title: "Say Hello in the Console",
  prompt:
    "Write your first program:\n\n1. Log the exact text `Hello, web!` (with the comma and exclamation mark).\n2. Log a second line — any sentence you like — using another console.log.\n3. Add a comment above your first log explaining what it does.",
  difficulty: "beginner",
  boilerplate: '// 1) log "Hello, web!" exactly\n\n// 2) log a second sentence\n',
  tests: [
    {
      name: "logs the exact greeting",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
try {
  new Function("console", code)(fakeConsole);
} catch (err) {
  throw new Error("Your code threw: " + err.message);
}
if (!logs.some((l) => l === "Hello, web!")) {
  throw new Error('Expected a log of exactly "Hello, web!" — check spelling, comma, and exclamation mark.');
}`,
      hint: 'console.log("Hello, web!");',
    },
    {
      name: "logs a second line",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (logs.length < 2) {
  throw new Error("Expected at least two console.log calls — got " + logs.length + ".");
}`,
      hint: "Add a second console.log with any sentence in quotes.",
    },
    {
      name: "includes a comment",
      code: `if (!code.includes("//")) {
  throw new Error("Add a comment starting with // somewhere in your code.");
}`,
      hint: "A comment looks like: // this logs a greeting",
    },
  ],
});

/* ── 4.2 Variables ───────────────────────────────────────────────────── */

writeLesson(
  "js-variables",
  "Variables: Naming Values",
  "let and const — how programs remember. Name a value once, reuse it everywhere, and learn the one rule professionals follow by default.",
  12,
  "beginner",
  ["variables-practice"],
  `
A **variable** is a named box for a value. Instead of repeating data, you store it
once and refer to it by name.

## Declaring variables

${T}${T}${T}js
const courseName = "Web Development Beginner";
let lessonsDone = 0;

lessonsDone = 1;      // let — value can change
${T}${T}${T}

- ${T}const${T} declares a variable that **cannot be reassigned**.
- ${T}let${T} declares one that can.

## The professional default: const

Use ${T}const${T} for everything, and switch to ${T}let${T} only when you
actually reassign. This makes code self-documenting: when a reader sees
${T}const${T}, they know the value never flips out from under them.

${T}${T}${T}js
const price = 19.99;
let total = 0;

total = price * 2;    // fine — total is let
price = 9.99;         // TypeError! const cannot be reassigned
${T}${T}${T}

## Names matter

Names are lowercase, descriptive, and use **camelCase** (first word lowercase,
later words capitalized):

${T}${T}${T}js
const firstName = "Ada";       // good
const x = "Ada";               // legal but meaningless
const first_name = "Ada";      // legal but not the JS convention
${T}${T}${T}

## Using variables

Once declared, the name *is* the value:

${T}${T}${T}js
const learner = "Ada";
console.log("Hello, " + learner + "!");   // Hello, Ada!
console.log(${T}Hello, ${D}{learner}!${T});       // Hello, Ada!  ← template literal
${T}${T}${T}

The second line is a **template literal**: backticks around the text, with
${T}${D}{ ... }${T} slots that drop variable values right into the string. You will
use these constantly.

## What you learned

- Variables are named values: ${T}const${T} (default) and ${T}let${T} (reassignable)
- camelCase names that describe the value
- Template literals: ${T}${D}{variable}${T} slots inside backtick strings

**Next:** the kinds of values variables can hold.
`,
);

writeChallenge("js-variables", {
  id: "variables-practice",
  title: "Store and Combine",
  prompt:
    "Practice variables and template literals:\n\n1. Declare a `const` called `learner` holding your name (a string).\n2. Declare a `let` called `lessonsDone` starting at 0, then reassign it to 3.\n3. Compute `const remaining = 15 - lessonsDone;`\n4. Log one sentence using a template literal that includes both the name and the remaining count — e.g. `Ada has 12 lessons left.`",
  difficulty: "beginner",
  boilerplate: "// 1) learner (const)\n\n// 2) lessonsDone (let), then reassign\n\n// 3) remaining\n\n// 4) template-literal sentence\n",
  tests: [
    {
      name: "learner is a const string",
      code: `const fn = new Function(code + "\\nreturn { learner, lessonsDone, remaining };");
const { learner } = fn();
if (typeof learner !== "string" || learner.length === 0) {
  throw new Error("learner must be a non-empty string.");
}
if (!/const\\s+learner/.test(code)) {
  throw new Error("Declare learner with const, not let.");
}`,
      hint: 'const learner = "Ada";',
    },
    {
      name: "lessonsDone is reassigned to 3",
      code: `const fn = new Function(code + "\\nreturn { learner, lessonsDone, remaining };");
const { lessonsDone, remaining } = fn();
if (lessonsDone !== 3) {
  throw new Error("lessonsDone should end up as 3 — declare it with let, then reassign.");
}
if (remaining !== 12) {
  throw new Error("remaining should be 15 - lessonsDone.");
}
if (!/let\\s+lessonsDone\\s*=\\s*0/.test(code)) {
  throw new Error("Start lessonsDone at 0 with let, then reassign it.");
}`,
      hint: "let lessonsDone = 0; lessonsDone = 3; const remaining = 15 - lessonsDone;",
    },
    {
      name: "sentence uses a template literal with both values",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
const sentence = logs.find((l) => l.includes("12"));
if (!sentence) {
  throw new Error("The logged sentence should mention 12 (the remaining count).");
}
const bt = String.fromCharCode(96);
if (!code.includes(bt)) {
  throw new Error("Build the sentence with a template literal (backticks).");
}`,
      hint: "console.log(`${learner} has ${remaining} lessons left.`);",
    },
  ],
});

/* ── 4.3 Types & Operators ───────────────────────────────────────────── */

writeLesson(
  "js-types-and-operators",
  "Types and Operators",
  "Six value types cover most beginner code — strings, numbers, booleans, null, undefined — plus the operators that combine them.",
  14,
  "beginner",
  ["types-and-operators"],
  `
Every value in JavaScript has a **type**. Six cover most beginner code.

## The primitives

~~~js
const name = "Ada";        // string — text in quotes
const year = 2026;         // number — integers and decimals alike
const pi = 3.14159;        // also a number
const isLive = true;       // boolean — true or false
let nothing = null;        // null — deliberately "no value"
let notSet;                // undefined — declared, never assigned
~~~

${T}null${T} and ${T}undefined${T} both mean "nothing here" — the difference is who
did it: ${T}null${T} is a deliberate choice by the programmer; ${T}undefined${T}
means the value was never set.

## Numbers and arithmetic

~~~js
const price = 19.99;
const quantity = 3;

price * quantity    // 59.97  (multiplication)
10 + 3              // 13
10 / 4              // 2.5
10 % 3              // 1   remainder — "% is the remainder operator"
~~~

${T}%${T} (remainder) is surprisingly useful: ${T}n % 2 === 0${T} tests whether a
number is even.

## Strings: joining and building

~~~js
const first = "Ada";
const last = "Lovelace";

first + " " + last                  // "Ada Lovelace" — + joins strings
${T}Full name: ${D}{first} ${D}{last}${T}   // template literal (backticks)
first.length                        // 3 — strings have properties too
name.toUpperCase()                  // "ADA" — and methods
~~~

## Comparisons → booleans

~~~js
const age = 20;

age >= 18        // true
age === 20       // true  — strict equality (three equals: always use this)
age !== 21       // true  — strict inequality
~~~

**Always use ${T}===${T} and ${T}!==${T}.** The loose versions (${T}==${T}) do
surprising type conversions — a classic bug source you will simply never need.

## Logic: &&, ||, !

~~~js
const age = 20;
const hasTicket = true;

age >= 18 && hasTicket   // true — AND: both sides must be true
age < 12 || age > 65     // false — OR: at least one side true
!hasTicket               // false — NOT: flips the boolean
~~~

## What you learned

- Six primitives; null (deliberate) vs undefined (not yet set)
- Arithmetic including the remainder ${T}%${T}
- Template literals build strings; ${T}===${T}/${T}!==${T} for comparisons
- ${T}&&${T}, ${T}||${T}, ${T}!${T} combine booleans

**Next:** programs that decide and repeat.
`,
);

writeChallenge("js-types-and-operators", {
  id: "types-and-operators",
  title: "Receipt Math",
  prompt:
    'A cart holds `const price = 19.99;` and `const quantity = 3;` (declare these yourself).\n\n1. Compute `const total = price * quantity;`\n2. Log a sentence built with a template literal that includes both the quantity and the total — e.g. "3 items cost 59.97".\n3. Log whether `total > 50` (a boolean).\n4. Log whether the order is big AND affordable: `total > 10 && total < 100`.',
  difficulty: "beginner",
  boilerplate:
    "const price = 19.99;\nconst quantity = 3;\n\n// 1) total\n\n// 2) sentence via template literal\n\n// 3) is it over 50?\n\n// 4) big AND affordable\n",
  tests: [
    {
      name: "total computed from the variables",
      code: `const fn = new Function(code + "\\nreturn { total };");
const { total } = fn();
if (total !== 59.97) {
  throw new Error("total should be price * quantity = 59.97.");
}
if (!/(const|let)\\s+total\\s*=\\s*price\\s*\\*\\s*quantity\\s*;/.test(code)) {
  throw new Error("Compute total from the variables: const total = price * quantity;");
}`,
      hint: "const total = price * quantity; — use the variables, not a hard-coded number.",
    },
    {
      name: "sentence uses a template literal with both values",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
try {
  new Function("console", code)(fakeConsole);
} catch (err) {
  throw new Error("Your code threw: " + err.message);
}
const sentence = logs.find((l) => l.includes("3") && l.includes("59.97"));
if (!sentence) {
  throw new Error('The logged sentence should contain both "3" and "59.97".');
}
const bt = String.fromCharCode(96);
if (!code.includes(bt)) {
  throw new Error("Build the sentence with a template literal (backticks).");
}`,
      hint: "console.log(`${quantity} items cost ${total}`);",
    },
    {
      name: "comparison and logic logged",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (!logs.some((l) => l === "true")) {
  throw new Error("Log the boolean comparisons — total > 50 should print true.");
}
if (!/&&/.test(code)) {
  throw new Error("Use the && operator for the combined condition.");
}`,
      hint: "console.log(total > 50); console.log(total > 10 && total < 100);",
    },
  ],
});

/* ── 4.4 Conditionals ────────────────────────────────────────────────── */

writeLesson(
  "js-conditionals",
  "Making Decisions: if / else",
  "Programs that choose: if, else if, and else — how code takes different paths based on data.",
  12,
  "beginner",
  ["grade-classifier"],
  `
So far every line of your code has run. **Conditionals** let programs choose.

## if / else if / else

~~~js
const score = 87;

if (score >= 90) {
  console.log("A");
} else if (score >= 80) {
  console.log("B");
} else if (score >= 70) {
  console.log("C");
} else {
  console.log("Keep practicing");
}
~~~

The conditions are checked top to bottom; the **first** truthy one wins and the
rest are skipped. The final ${T}else${T} catches everything the earlier branches
missed.

## Truthiness

Conditions do not need to be booleans — JavaScript converts them:

- **Falsy:** ${T}false${T}, ${T}0${T}, ${T}""${T} (empty string), ${T}null${T},
  ${T}undefined${T}, ${T}NaN${T}
- **Truthy:** everything else — including ${T}"0"${T}, ${T}"false"${T}, and
  ${T}[]${T}

~~~js
const name = "";      // falsy!

if (name) {
  console.log("Hello, " + name);
} else {
  console.log("Please enter your name");
}
~~~

This pattern — *if the value exists, use it, otherwise handle the missing case* —
is everywhere in real code.

## Nesting and combining

~~~js
const age = 15;
const withAdult = true;

if (age >= 18 || withAdult) {
  console.log("You can enter");
} else {
  console.log("Sorry, adults only");
}
~~~

Prefer combining conditions with ${T}&&${T}/${T}||${T} over deep nesting — flat
reads better.

## What you learned

- ${T}if${T} / ${T}else if${T} / ${T}else${T}: first matching branch wins
- Falsy values: ${T}false, 0, "", null, undefined, NaN${T}
- Combine conditions with logical operators instead of nesting deeply

**Next:** doing things repeatedly — loops.
`,
);

writeChallenge("js-conditionals", {
  id: "grade-classifier",
  title: "Write a Grader",
  prompt:
    "Write a function `grade(score)` that returns a letter grade string:\n\n- 90 or above returns \"A\"\n- 80–89 returns \"B\"\n- 70–79 returns \"C\"\n- anything below returns \"Keep practicing\"\n\nThen log the result of `grade(85)` and `grade(92)`.",
  difficulty: "beginner",
  boilerplate: "// grade(score) returns the letter as a STRING\n\n\n// log two examples\n",
  tests: [
    {
      name: "returns the right grade for each band",
      code: `const fn = new Function(code + "\\nreturn { grade };");
const { grade } = fn();
if (grade(95) !== "A") throw new Error('grade(95) should return "A".');
if (grade(90) !== "A") throw new Error('grade(90) should return "A" (90 or above).');
if (grade(85) !== "B") throw new Error('grade(85) should return "B".');
if (grade(72) !== "C") throw new Error('grade(72) should return "C".');
if (grade(8) !== "Keep practicing") throw new Error('grade(8) should return "Keep practicing".');`,
      hint: 'if (score >= 90) { return "A"; } else if (score >= 80) { return "B"; } ...',
    },
    {
      name: "returns (does not just log)",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
const fn = new Function("console", code + "\\nreturn { grade };");
const { grade } = fn(fakeConsole);
const direct = grade(100);
if (direct !== "A") {
  throw new Error("grade must RETURN the letter — a return value, not just a console.log.");
}`,
      hint: "Return the string from inside each branch: return \"A\"; — logging is not returning.",
    },
    {
      name: "logs two examples",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
new Function("console", code)(fakeConsole);
if (!logs.some((l) => l === "B") || !logs.some((l) => l === "A")) {
  throw new Error("Log grade(85) and grade(92) — the console should show B and A.");
}`,
      hint: "console.log(grade(85)); console.log(grade(92));",
    },
  ],
});

/* ── 4.5 Loops ───────────────────────────────────────────────────────── */

writeLesson(
  "js-loops",
  "Loops: Repeating Work",
  "for and while — make the computer do the boring thousand times, and defuse the classic off-by-one trap.",
  14,
  "beginner",
  ["countdown-and-sum"],
  `
Computers shine at repetition. A **loop** runs the same block again with small
changes each pass.

## The for loop

~~~js
for (let i = 1; i <= 5; i++) {
  console.log("Visitor number " + i);
}
~~~

Three parts, separated by semicolons:

1. **Start:** ${T}let i = 1${T} — runs once, before anything else
2. **Condition:** ${T}i <= 5${T} — checked before every pass; loop stops when false
3. **Step:** ${T}i++${T} — runs after every pass (adds 1)

So this logs 1, 2, 3, 4, 5 — five passes.

## Counting from 0 — the classic trap

Arrays (next lesson) start at index **0**, so most loops look like:

~~~js
for (let i = 0; i < 5; i++) {   // 0,1,2,3,4 — exactly 5 passes
  console.log(i);
}
~~~

Note the condition: ${T}i < 5${T}, not ${T}i <= 5${T}. Starting at 0 with
${T}<${T} gives exactly 5 passes; mixing up the two is the most common beginner
loop bug. Check yours against this rule every time.

## while — loop until something changes

~~~js
let cups = 3;

while (cups > 0) {
  console.log("Cups left: " + cups);
  cups = cups - 1;      // something must change, or the loop never ends!
}
~~~

${T}while${T} is best when you do not know how many passes you need. If the
condition never becomes false you get an **infinite loop** — the tab freezes.

## Looping with a purpose: accumulating

~~~js
let total = 0;
for (let n = 1; n <= 10; n++) {
  total = total + n;    // add each number into the running total
}
console.log(total);     // 55
~~~

The pattern — declare an accumulator *before* the loop, update it *inside* — powers
sums, counting, building strings, and most data processing you will do this module.

## What you learned

- ${T}for${T}: start; condition; step
- Count from 0 with ${T}i < n${T}; from 1 through n with ${T}i <= n${T}
- ${T}while${T} repeats until its condition goes false — always change something inside
- Accumulator pattern: declare before, update inside

**Next:** bundling code into reusable functions.
`,
);

writeChallenge("js-loops", {
  id: "countdown-and-sum",
  title: "Countdown and Total",
  prompt:
    "Two loops:\n\n1. Write a function `countdown(start)` that logs each number from `start` down to 1 (one per line) using a loop.\n2. Write a function `sumUpTo(n)` that RETURNS the sum of all whole numbers from 1 to n (use an accumulator loop, not a hard-coded answer).\n\nLog `sumUpTo(10)` — it should print 55.",
  difficulty: "intermediate",
  boilerplate: "// 1) countdown(start) — logs start..1\n\n\n// 2) sumUpTo(n) — returns 1+2+...+n\n\n\n// log sumUpTo(10)\n",
  tests: [
    {
      name: "countdown logs start down to 1",
      code: `const logs = [];
const fakeConsole = { log: (...a) => logs.push(a.map(String).join(" ")) };
const fn = new Function("console", code + "\\nreturn { countdown, sumUpTo };");
const { countdown } = fn(fakeConsole);
logs.length = 0;
countdown(3);
const seq = logs.join(",");
if (seq !== "3,2,1") {
  throw new Error('countdown(3) should log 3, 2, 1 in that order — got "' + seq + '".');
}`,
      hint: "for (let i = start; i >= 1; i--) { console.log(i); }",
    },
    {
      name: "sumUpTo returns the real sum",
      code: `const fn = new Function(code + "\\nreturn { countdown, sumUpTo };");
const { sumUpTo } = fn();
if (sumUpTo(10) !== 55) throw new Error("sumUpTo(10) should be 55.");
if (sumUpTo(4) !== 10) throw new Error("sumUpTo(4) should be 10 — not a hard-coded value.");
if (sumUpTo(1) !== 1) throw new Error("sumUpTo(1) should be 1.");
if (sumUpTo(100) !== 5050) throw new Error("sumUpTo(100) should be 5050 — use a loop.");`,
      hint: "let total = 0; for (let n = 1; n <= max; n++) { total = total + n; } return total;",
    },
    {
      name: "sumUpTo actually loops",
      code: `if (!/for\\s*\\(|while\\s*\\(/.test(code)) {
  throw new Error("Use a for or while loop to compute the sum.");
}`,
      hint: "The accumulator pattern needs a loop — no shortcuts like n*(n+1)/2 for this one.",
    },
  ],
});
