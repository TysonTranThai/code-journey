/**
 * Author CSS practice content (Course 1 revision, wave 2).
 *
 * Writes practice set + challenge JSON files and appends their reference
 * solutions to practice-solutions.mjs (imported by the QA harness).
 * Each challenge is verified immediately after authoring:
 *   reference solution passes all tests; a wrong solution fails ≥1 test.
 *
 * Run: node scripts/content-authoring/author-css-practices.mjs
 */
import { mkdirSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const BASE =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/css-foundations/practices";
const SOLUTIONS_FILE = "scripts/content-authoring/practice-solutions.mjs";
const P = (id) => path.join(BASE, id, "challenges");

const SETS = [
  {
    file: "css-selectors-practice.json",
    id: "css-selectors-practice",
    title: "Selectors Under Command",
    description:
      "Aim styles precisely: element, class, id, and descendant selectors — then override one specific heading without touching the rest.",
    afterLesson: "selectors-and-cascade",
    minutes: 15,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-basic-selectors",
        title: "Element, Class, and ID Selectors",
        prompt: `Style the page three ways at once:

- Every \`p\` gets \`color: dimgray\`.
- Every element with class \`note\` gets \`background-color: lightyellow\`.
- The element with id \`tagline\` gets \`font-style: italic\`.

Rules:
- One rule per target — no combined selectors.`,
        difficulty: "beginner",
        boilerplate: "<!-- CSS only: write the three rules -->\n",
        tests: [
          {
            name: "p elements get dimgray",
            code: `if (!/<style>[\\s\\S]*p\\s*\\{[^}]*color\\s*:\\s*dimgray\\s*;[^}]*\\}[\\s\\S]*<\\/style>/i.test(code) && !/^(?!\\s*<)[\\s\\S]*p\\s*\\{[^}]*color\\s*:\\s*dimgray/i.test(code)) {
  throw new Error("Add a rule: p { color: dimgray; }");
}`,
            hint: "p { color: dimgray; } — an element selector styles every paragraph.",
          },
          {
            name: "class .note gets its background",
            code: `if (!/\\.note\\s*\\{[^}]*background-color\\s*:\\s*lightyellow\\s*;/i.test(code)) {
  throw new Error("Add a rule: .note { background-color: lightyellow; }");
}`,
            hint: "A class selector starts with a dot: .note { background-color: lightyellow; }",
          },
          {
            name: "id #tagline goes italic",
            code: `if (!/#tagline\\s*\\{[^}]*font-style\\s*:\\s*italic\\s*;/i.test(code)) {
  throw new Error("Add a rule: #tagline { font-style: italic; }");
}`,
            hint: "An id selector starts with a hash: #tagline { font-style: italic; }",
          },
        ],
      },
      {
        id: "practice-descendant-selector",
        title: "Style Only the Links in the Nav",
        prompt: `The page has links everywhere, but only the ones inside \`nav\` should look like nav links. Write ONE rule using a descendant selector: links inside \`nav\` get \`color: teal\` and \`text-decoration: none\`. Links elsewhere must not be affected by your rule.

Rules:
- Exactly one rule.
- Descendant selector: \`nav a\`.`,
        difficulty: "beginner",
        boilerplate: "<!-- One descendant-selector rule -->\n",
        tests: [
          {
            name: "one rule with a descendant selector",
            code: `const rules = code.match(/[^{}]+\\{[^}]*\\}/g) ?? [];
if (rules.length !== 1) throw new Error(\`Exactly one rule expected, found \${rules.length}.\`);
if (!/nav\\s+a(?!\\w)/i.test(rules[0])) {
  throw new Error("Use the descendant selector: nav a { … }");
}`,
            hint: "nav a { … } reads 'every a inside nav'.",
          },
          {
            name: "teal and no underline",
            code: `const rule = code.match(/\\{[^}]*\\}/)[0];
if (!/color\\s*:\\s*teal\\s*;/i.test(rule)) throw new Error("The rule needs color: teal;");
if (!/text-decoration\\s*:\\s*none\\s*;/i.test(rule)) throw new Error("The rule needs text-decoration: none;");`,
            hint: "Both declarations inside the one rule: color: teal; text-decoration: none;",
          },
          {
            name: "no bare a selector",
            code: `if (/(^|[^.\\w])a\\s*\\{/i.test(code.replace(/\\w+\\s*a\\s*\\{/g, ""))) {
  throw new Error("Found a bare a { … } rule — that would style every link on the page.");
}`,
            hint: "A bare a { … } styles all links. Scope it: nav a { … }",
          },
        ],
      },
      {
        id: "practice-override-one-heading",
        title: "Override Just One Heading",
        prompt: `Three \`h2\` headings share a style: \`h2 { color: seagreen; }\` — already written for you. The heading with id \`featured\` must instead be \`crimson\`, and your override must beat the element selector.

Rules:
- Keep the given rule untouched.
- Add one rule that wins over \`h2\` for \`#featured\`.`,
        difficulty: "beginner",
        boilerplate: `<style>
h2 {
  color: seagreen;
}
/* your override here */
</style>

<h2>Fresh bread</h2>
<h2 id="featured">Sourdough of the week</h2>
<h2>Croissants</h2>
`,
        tests: [
          {
            name: "original rule survives",
            code: `if (!/h2\\s*\\{[^}]*color\\s*:\\s*seagreen\\s*;/i.test(code)) {
  throw new Error("Keep the original h2 { color: seagreen; } rule.");
}`,
            hint: "Don't modify the given rule — add, don't replace.",
          },
          {
            name: "#featured override wins",
            code: `if (!/#featured\\s*\\{[^}]*color\\s*:\\s*crimson\\s*;/i.test(code)) {
  throw new Error("Add: #featured { color: crimson; } — an id beats an element selector.");
}`,
            hint: "#featured { color: crimson; } — id specificity (1,0,0) beats element (0,0,1).",
          },
          {
            name: "no !important shortcuts",
            code: `if (/!important/i.test(code)) {
  throw new Error("No !important — win on specificity, which is exactly the lesson here.");
}`,
            hint: "The id selector alone outranks the element selector. No !important needed.",
          },
        ],
      },
    ],
  },
  {
    file: "css-box-model-practice.json",
    id: "css-box-model-practice",
    title: "Box Model Workouts",
    description:
      "Padding, border, and margin on real components — including the border-box reset that makes width mean width.",
    afterLesson: "css-box-model",
    minutes: 15,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-card-spacing",
        title: "Space Out a Card",
        prompt: `Give \`.card\` breathing room: \`padding: 1.5rem\` inside, a \`border: 1px solid silver\`, and \`margin: 1rem 0\` outside. Also set \`border-radius: 8px\` for soft corners.

Rules:
- All four declarations on \`.card\`.`,
        difficulty: "beginner",
        boilerplate: '<!-- Style the card -->\n\n<div class="card">A cozy little card</div>\n',
        tests: [
          {
            name: "padding 1.5rem",
            code: `if (!/\\.card\\s*\\{[^}]*padding\\s*:\\s*1\\.5rem\\s*;/i.test(code)) throw new Error("Add padding: 1.5rem to .card.");`,
            hint: "padding: 1.5rem — space inside the border.",
          },
          {
            name: "border 1px solid silver",
            code: `if (!/\\.card\\s*\\{[^}]*border\\s*:\\s*1px\\s+solid\\s+silver\\s*;/i.test(code)) throw new Error("Add border: 1px solid silver to .card.");`,
            hint: "border: 1px solid silver — width, style, color in one declaration.",
          },
          {
            name: "margin 1rem 0",
            code: `if (!/\\.card\\s*\\{[^}]*margin\\s*:\\s*1rem\\s+0\\s*;/i.test(code)) throw new Error("Add margin: 1rem 0 to .card.");`,
            hint: "margin: 1rem 0 — vertical spacing, none horizontal.",
          },
          {
            name: "rounded corners",
            code: `if (!/\\.card\\s*\\{[^}]*border-radius\\s*:\\s*8px\\s*;/i.test(code)) throw new Error("Add border-radius: 8px to .card.");`,
            hint: "border-radius: 8px rounds every corner.",
          },
        ],
      },
      {
        id: "practice-border-box-reset",
        title: "Make Width Mean Width",
        prompt: `A \`.box\` is styled \`width: 200px; padding: 20px; border: 4px solid dimgray;\` — but the element renders wider than 200px. Fix it the professional way: add the universal \`box-sizing: border-box\` reset (with the \*/\` before/after pseudo selectors) so the declared width includes padding and border.

Rules:
- Add the reset: \`*, *::before, *::after { box-sizing: border-box; }\`.
- Don't change the .box rule.`,
        difficulty: "beginner",
        boilerplate: `<style>
.box {
  width: 200px;
  padding: 20px;
  border: 4px solid dimgray;
}
</style>

<div class="box">200 means 200</div>
`,
        tests: [
          {
            name: "universal border-box reset present",
            code: `if (!/\\*\\s*,\\s*\\*::before\\s*,\\s*\\*::after\\s*\\{[^}]*box-sizing\\s*:\\s*border-box\\s*;/i.test(code)) {
  throw new Error("Add the reset: *, *::before, *::after { box-sizing: border-box; }");
}`,
            hint: "*, *::before, *::after { box-sizing: border-box; } — the standard first rule of a stylesheet.",
          },
          {
            name: "box rule untouched",
            code: `if (!/\\.box\\s*\\{[^}]*width\\s*:\\s*200px\\s*;[^}]*padding\\s*:\\s*20px\\s*;[^}]*border\\s*:\\s*4px\\s+solid\\s+dimgray\\s*;/i.test(code)) {
  throw new Error("The .box rule changed — this exercise adds the reset, not edits the box.");
}`,
            hint: "Leave .box exactly as it is; the reset fixes the math.",
          },
          {
            name: "reset is not scoped to .box",
            code: `const rule = code.match(/[^{}]*\\*\\s*,[^{]*\\{[^}]*box-sizing[^}]*\\}/i)[0];
if (/\\.box/.test(rule)) throw new Error("The reset must be universal (starting with *), not scoped to .box.");`,
            hint: "The reset starts with *, *::before, *::after — a universal selector.",
          },
        ],
      },
      {
        id: "practice-margin-cleanup",
        title: "Debug: The Mystery Gap",
        prompt: `Two cards sit side by side but there's an unwanted 2rem gap between them. One card carries \`margin-right: 2rem\` — remove that declaration entirely (don't set it to 0; delete the line). Leave everything else alone.

Rules:
- The \`.card + .card\` rule keeps its \`margin-left: 1rem\`.
- The \`margin-right: 2rem\` line is gone.`,
        difficulty: "beginner",
        boilerplate: `<style>
.card {
  width: 200px;
  background: lavender;
}

.card + .card {
  margin-left: 1rem;
}
</style>

<div class="card">One</div>
<div class="card">Two</div>
`,
        tests: [
          {
            name: "unwanted margin-right removed",
            code: `if (/margin-right\\s*:\\s*2rem/i.test(code)) {
  throw new Error("margin-right: 2rem is still there — delete the declaration.");
}`,
            hint: "Delete the whole margin-right: 2rem; line from the first card's rule.",
          },
          {
            name: "adjacent-sibling spacing survives",
            code: `if (!/\\.card\\s*\\+\\s*\\.card\\s*\\{[^}]*margin-left\\s*:\\s*1rem\\s*;/i.test(code)) {
  throw new Error("Keep .card + .card { margin-left: 1rem; } — that's the intended spacing.");
}`,
            hint: "The .card + .card rule with margin-left: 1rem stays exactly as it is.",
          },
          {
            name: "card base rule intact",
            code: `if (!/\\.card\\s*\\{[^}]*width\\s*:\\s*200px\\s*;[^}]*background\\s*:\\s*lavender\\s*;/i.test(code)) {
  throw new Error("The .card base rule changed — only the stray margin-right line should disappear.");
}`,
            hint: "width: 200px and background: lavender stay on .card.",
          },
        ],
      },
    ],
  },
];

// ── Reference + wrong solutions (validated immediately below) ──
const REFS = {
  "practice-basic-selectors": `<style>
p {
  color: dimgray;
}

.note {
  background-color: lightyellow;
}

#tagline {
  font-style: italic;
}
</style>`,
  "practice-descendant-selector": `<style>
nav a {
  color: teal;
  text-decoration: none;
}
</style>`,
  "practice-override-one-heading": `<style>
h2 {
  color: seagreen;
}

#featured {
  color: crimson;
}
</style>

<h2>Fresh bread</h2>
<h2 id="featured">Sourdough of the week</h2>
<h2>Croissants</h2>`,
  "practice-card-spacing": `<style>
.card {
  padding: 1.5rem;
  border: 1px solid silver;
  margin: 1rem 0;
  border-radius: 8px;
}
</style>

<div class="card">A cozy little card</div>`,
  "practice-border-box-reset": `<style>
*, *::before, *::after {
  box-sizing: border-box;
}

.box {
  width: 200px;
  padding: 20px;
  border: 4px solid dimgray;
}
</style>

<div class="box">200 means 200</div>`,
  "practice-margin-cleanup": `<style>
.card {
  width: 200px;
  background: lavender;
}

.card + .card {
  margin-left: 1rem;
}
</style>

<div class="card">One</div>
<div class="card">Two</div>`,
};

const WRONGL = {
  "practice-basic-selectors": "p { color: dimgray; }",
  "practice-descendant-selector": "a { color: teal; text-decoration: none; }",
  "practice-override-one-heading": "h2 { color: seagreen; }\nh2 { color: crimson; }",
  "practice-card-spacing": ".card { padding: 10px; }",
  "practice-border-box-reset": ".box { box-sizing: border-box; }",
  "practice-margin-cleanup": ".card { margin-right: 2rem; }",
};

function runTest(testCode, studentCode) {
  const sandbox = { code: studentCode, result: undefined, setTimeout, clearTimeout };
  const ctx = vm.createContext(sandbox);
  return new vm.Script(
    `(async () => { try { ${testCode}\n result = "PASS"; } catch (err) { result = "FAIL: " + (err && err.message ? err.message : String(err)); } })()`,
  )
    .runInContext(ctx, { awaitPromise: true })
    .then(() => sandbox.result);
}

let pending = "";
for (const set of SETS) {
  mkdirSync(path.join(BASE, set.id, "challenges"), { recursive: true });
  const setPath = path.join(BASE, set.file);
  if (existsSync(setPath)) {
    console.log(`SKIP ${set.file} (exists)`);
    for (const ch of set.challenges)
      pending += `R[${JSON.stringify(ch.id)}] = ${JSON.stringify(REFS[ch.id])};\nW[${JSON.stringify(ch.id)}] = ${JSON.stringify(WRONGL[ch.id])};\n`;
    continue;
  }
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
  for (const ch of set.challenges) {
    writeFileSync(path.join(P(set.id), `${ch.id}.json`), JSON.stringify(ch, null, 2) + "\n");
    pending += `R[${JSON.stringify(ch.id)}] = ${JSON.stringify(REFS[ch.id])};\nW[${JSON.stringify(ch.id)}] = ${JSON.stringify(WRONGL[ch.id])};\n`;
    // immediate verification
    const results = [];
    for (const t of ch.tests) results.push(await runTest(t.code, REFS[ch.id]));
    const refOk = results.every((r) => r === "PASS");
    const wrongResults = [];
    for (const t of ch.tests) wrongResults.push(await runTest(t.code, WRONGL[ch.id]));
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
appendFileSync(SOLUTIONS_FILE, pending);
console.log(
  `appended ${pending.split("\n").filter((l) => l.startsWith("R[")).length} solution pairs to ${SOLUTIONS_FILE}`,
);
