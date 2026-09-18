/**
 * Author Git + web-architecture practice content (Course 1 revision, wave 4).
 *
 * Run: node scripts/content-authoring/author-git-arch-practices.mjs
 */
import { mkdirSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const SOLUTIONS_FILE = "scripts/content-authoring/practice-solutions.mjs";

const GIT_BASE =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/developer-tools-git-and-github/practices";
const ARCH_BASE =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/how-modern-websites-work/practices";

const SETS = [
  {
    base: GIT_BASE,
    file: "git-workflow-practice.json",
    id: "git-workflow-practice",
    title: "Git Workflow Drills",
    description:
      "Type the commands you'll use every day: stage and commit, branch and merge, recover from a mistake.",
    afterLesson: "git-version-control",
    minutes: 12,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-save-point",
        title: "Create a Save Point",
        prompt: `Fill the object with the exact commands:
- \`stage\`: the command that stages every change.
- \`commit\`: the command that records a save point with the message \`"Add navigation"\`.
- \`check\`: the command that shows what's staged before you commit.`,
        difficulty: "beginner",
        boilerplate: `const workflow = {
  check: "",
  stage: "",
  commit: "",
};
`,
        tests: [
          {
            name: "stage everything",
            code: `const fn = new Function(code + "\\nreturn workflow;");
const w = fn();
if (w.stage !== "git add .") throw new Error("stage should be: git add .");`,
            hint: "git add . stages every change in the project.",
          },
          {
            name: "commit with a message",
            code: `const fn = new Function(code + "\\nreturn workflow;");
const w = fn();
if (!/^git commit -m ["']Add navigation["']$/.test(w.commit)) {
  throw new Error('commit should be: git commit -m "Add navigation"');
}`,
            hint: 'git commit -m "Add navigation" — messages explain the why.',
          },
          {
            name: "check before committing",
            code: `const fn = new Function(code + "\\nreturn workflow;");
const w = fn();
if (w.check !== "git status") throw new Error("check should be: git status");`,
            hint: "git status shows what's staged and what isn't.",
          },
        ],
      },
      {
        id: "practice-undo-commit",
        title: "Undo, Safely",
        prompt: `You committed too early. Fill the object:
- \`redo\`: the command that creates a NEW commit reversing your last one (never rewrite shared history).
- \`inspect\`: the command that shows the commit history.`,
        difficulty: "beginner",
        boilerplate: `const undo = {
  inspect: "",
  redo: "",
};
`,
        tests: [
          {
            name: "inspect the history",
            code: `const fn = new Function(code + "\\nreturn undo;");
const u = fn();
if (u.inspect !== "git log") throw new Error("inspect should be: git log");`,
            hint: "git log lists the commits.",
          },
          {
            name: "revert, not reset",
            code: `const fn = new Function(code + "\\nreturn undo;");
const u = fn();
if (!/^git revert HEAD$/.test(u.redo)) {
  throw new Error("redo should be: git revert HEAD — a new commit that undoes the old one.");
}`,
            hint: "git revert HEAD is safe for shared branches — it adds an inverse commit.",
          },
          {
            name: "no history rewriting",
            code: `if (/git\\s+reset\\s+--hard|push\\s+--force|push\\s+-f/.test(code)) {
  throw new Error("reset --hard and force-push rewrite history — banned on shared work.");
}`,
            hint: "Revert adds history; reset/force-push destroys it. On shared branches: revert.",
          },
        ],
      },
    ],
  },
  {
    base: ARCH_BASE,
    file: "web-architecture-practice.json",
    id: "web-architecture-practice",
    title: "Architecture in Real Scenarios",
    description:
      "Apply client/server thinking: classify features by where they run, then trace what happens when a user hits a protected page.",
    afterLesson: "frontend-backend",
    minutes: 12,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-classify-features",
        title: "Where Does It Run?",
        prompt: `For each feature, answer \`"frontend"\` or \`"backend"\`:
- \`cartAnimation\`: animating items into a shopping cart icon.
- \`chargeCard\`: charging the customer's credit card.
- \`stockCheck\`: checking the warehouse database for stock.
- \`darkMode\`: toggling the site's color theme.`,
        difficulty: "beginner",
        boilerplate: `const answers = {
  cartAnimation: "",
  chargeCard: "",
  stockCheck: "",
  darkMode: "",
};
`,
        tests: [
          {
            name: "browser-only work stays frontend",
            code: `const fn = new Function(code + "\\nreturn answers;");
const a = fn();
if (a.cartAnimation !== "frontend") throw new Error("cartAnimation is frontend — it's pure visual work in the browser.");
if (a.darkMode !== "frontend") throw new Error("darkMode is frontend — a theme toggle needs no server.");`,
            hint: "If it only moves pixels in the browser, it's frontend.",
          },
          {
            name: "trust and data stay backend",
            code: `const fn = new Function(code + "\\nreturn answers;");
const a = fn();
if (a.chargeCard !== "backend") throw new Error("chargeCard is backend — money must never be handled in the browser.");
if (a.stockCheck !== "backend") throw new Error("stockCheck is backend — the database is on the server side.");`,
            hint: "Anything involving secrets, money, or databases runs on the server.",
          },
        ],
      },
      {
        id: "practice-request-trace",
        title: "Trace a Protected Request",
        prompt: `A logged-out visitor opens a members-only page. Order the steps: put the strings \`"browser requests page"\`, \`"server checks session"\`, \`"no session found"\`, \`"redirect to login"\` into the array in the order they happen.`,
        difficulty: "beginner",
        boilerplate: "const trace = [\n  // four steps, in order\n];\n",
        tests: [
          {
            name: "all four steps present",
            code: `const fn = new Function(code + "\\nreturn trace;");
const t = fn();
const expected = ["browser requests page", "server checks session", "no session found", "redirect to login"];
for (const step of expected) {
  if (!t.includes(step)) throw new Error(\`Missing step: \${step}\`);
}`,
            hint: "All four strings must appear in the array.",
          },
          {
            name: "steps in the right order",
            code: `const fn = new Function(code + "\\nreturn trace;");
const t = fn();
const expected = ["browser requests page", "server checks session", "no session found", "redirect to login"];
if (JSON.stringify(t) !== JSON.stringify(expected)) {
  throw new Error("Order: request → session check → no session → redirect.");
}`,
            hint: "The browser asks first; the server decides last. Check before redirect.",
          },
        ],
      },
    ],
  },
];

const REFS = {
  "practice-save-point": `const workflow = {
  check: "git status",
  stage: "git add .",
  commit: 'git commit -m "Add navigation"',
};`,
  "practice-undo-commit": `const undo = {
  inspect: "git log",
  redo: "git revert HEAD",
};`,
  "practice-classify-features": `const answers = {
  cartAnimation: "frontend",
  chargeCard: "backend",
  stockCheck: "backend",
  darkMode: "frontend",
};`,
  "practice-request-trace": `const trace = [
  "browser requests page",
  "server checks session",
  "no session found",
  "redirect to login",
];`,
};

const WRONGL = {
  "practice-save-point": `const workflow = { check: "", stage: "", commit: "" };`,
  "practice-undo-commit": `const undo = { inspect: "git log", redo: "git reset --hard" };`,
  "practice-classify-features": `const answers = { cartAnimation: "backend", chargeCard: "frontend", stockCheck: "frontend", darkMode: "backend" };`,
  "practice-request-trace": `const trace = ["no session found", "redirect to login", "browser requests page", "server checks session"];`,
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

let appended = 0;
for (const set of SETS) {
  mkdirSync(path.join(set.base, set.id, "challenges"), { recursive: true });
  const setPath = path.join(set.base, set.file);
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
    const chPath = path.join(set.base, set.id, "challenges", `${ch.id}.json`);
    if (!existsSync(chPath)) {
      writeFileSync(chPath, JSON.stringify(ch, null, 2) + "\n");
    }
    appendFileSync(
      SOLUTIONS_FILE,
      `R[${JSON.stringify(ch.id)}] = ${JSON.stringify(REFS[ch.id])};\nW[${JSON.stringify(ch.id)}] = ${JSON.stringify(WRONGL[ch.id])};\n`,
    );
    appended++;
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
console.log(`appended ${appended} solution pairs`);
