/**
 * Author JavaScript practice content (Course 1 revision, wave 3).
 * Same contract as the CSS authoring scripts.
 *
 * Run: node scripts/content-authoring/author-js-practices.mjs
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
    file: "js-variables-practice.json",
    id: "js-variables-practice",
    title: "Variables at Work",
    description:
      "Declare, reassign, and combine: const versus let, template literals, and a small shopping-total computation.",
    afterLesson: "js-variables",
    minutes: 12,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-const-vs-let",
        title: "const or let?",
        prompt: `Declare a constant \`firstName\` with the value \`"Ada"\`, and a \`let\` variable \`score\` starting at 0 that you then reassign to 42. Log both on one line using a template literal: \`Ada: 42\`.

Rules:
- \`firstName\` never changes — \`const\`.
- \`score\` is reassigned — \`let\`.`,
        difficulty: "beginner",
        boilerplate: "// Declare firstName and score, reassign score, then log them\n",
        tests: [
          {
            name: "const firstName holds Ada",
            code: `if (!/const\\s+firstName\\s*=\\s*["']Ada["']\\s*;/.test(code)) {
  throw new Error("Declare: const firstName = \\"Ada\\";");
}`,
            hint: 'const firstName = "Ada"; — constants can\'t be reassigned.',
          },
          {
            name: "let score reassigned to 42",
            code: `if (!/let\\s+score\\s*=\\s*0\\s*;/.test(code)) throw new Error("Start score at 0 with let.");
if (!/score\\s*=\\s*42\\s*;/.test(code)) throw new Error("Reassign score to 42 (without const/let the second time).");`,
            hint: "let score = 0; then later score = 42; — reassignment without a new declaration.",
          },
          {
            name: "template literal prints Ada: 42",
            code: `if (!/console\\.log\\(\\s*\`[^\\x60]*\\$\\{\\s*firstName\\s*\\}[^\\x60]*\\$\\{\\s*score\\s*\\}[^\\x60]*\`\\s*\\)/.test(code)) {
  throw new Error("Log with a template literal: console.log(\\\`\\\${firstName}: \\\${score}\\\`);");
}`,
            hint: "Backticks + ${…} interpolation: console.log(`${firstName}: ${score}`);",
          },
        ],
      },
      {
        id: "practice-shopping-total",
        title: "Compute the Shopping Total",
        prompt: `Given \`const price = 4.5\` and \`const quantity = 3\`, compute \`total\` and log a sentence using the variables, like \`3 items cost 13.5\`. Then log whether the total is more than 10 (a boolean).

Rules:
- Use arithmetic on the variables — no hard-coded 13.5.`,
        difficulty: "beginner",
        boilerplate:
          "const price = 4.5;\nconst quantity = 3;\n// compute total, log the sentence, log the comparison\n",
        tests: [
          {
            name: "total is price times quantity",
            code: `const totalDecl = code.match(/(const|let)\\s+total\\s*=\\s*([^;]+);/);
if (!totalDecl) throw new Error("Declare a total variable.");
if (!/price\\s*\\*\\s*quantity|quantity\\s*\\*\\s*price/.test(totalDecl[2])) {
  throw new Error("Compute total from price * quantity — don't hard-code the result.");
}`,
            hint: "const total = price * quantity; — the computer does the math.",
          },
          {
            name: "logs a sentence using the variables",
            code: `if (!/console\\.log\\([^)]*\\$\\{\\s*(quantity|total|price)\\s*\\}[^)]*\\)/.test(code) && !/console\\.log\\([^)]*\\+\\s*(quantity|total|price)/.test(code)) {
  throw new Error("Log a sentence that includes the variables (template literal or concatenation).");
}`,
            hint: "console.log(`${quantity} items cost ${total}`);",
          },
          {
            name: "logs the boolean comparison",
            code: `const logs = code.match(/console\\.log\\(([^;]+)\\);/g) ?? [];
const compares = logs.some((l) => /\\\$\\{[^}]*total[^}]*\\}\\s*>\\s*10|total\\s*>\\s*10/.test(l));
if (!compares) throw new Error("Log total > 10 somewhere — comparison expressions produce booleans.");`,
            hint: "console.log(total > 10); prints true or false.",
          },
        ],
      },
    ],
  },
  {
    file: "js-conditionals-practice.json",
    id: "js-conditionals-practice",
    title: "Decisions in Code",
    description:
      "Branch on values: a grade classifier, then refactoring chained else-ifs you didn't write but must understand.",
    afterLesson: "js-conditionals",
    minutes: 14,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-grade-gates",
        title: "Grade Gates",
        prompt: `Write \`function grade(score)\` that returns:
- \`"A"\` for 90 or more,
- \`"B"\` for 80–89,
- everything else \`"Keep practicing"\`.

Log the results for 92 and 55.

Rules:
- Use if / else if / else — the order of the checks matters.`,
        difficulty: "beginner",
        boilerplate:
          "function grade(score) {\n  // your branches here\n}\nconsole.log(grade(92));\nconsole.log(grade(55));\n",
        tests: [
          {
            name: "A for 90+",
            code: `const fn = new Function(code + "\\nreturn grade;");
if (fn()(92) !== "A") throw new Error("grade(92) should return 'A'.");
if (fn()(90) !== "A") throw new Error("grade(90) should also return 'A' — the gate is >= 90.");`,
            hint: 'if (score >= 90) return "A"; — remember 90 itself is an A.',
          },
          {
            name: "B for 80–89",
            code: `const fn = new Function(code + "\\nreturn grade;");
if (fn()(85) !== "B") throw new Error("grade(85) should return 'B'.");
if (fn()(80) !== "B") throw new Error("grade(80) should return 'B' too.");`,
            hint: 'else if (score >= 80) return "B"; — only reached when the first branch failed.',
          },
          {
            name: "kind fallback for everything else",
            code: `const fn = new Function(code + "\\nreturn grade;");
if (fn()(55) !== "Keep practicing") throw new Error("grade(55) should return 'Keep practicing'.");
if (fn()(0) !== "Keep practicing") throw new Error("grade(0) should also land in the fallback.");`,
            hint: 'The final else catches every remaining score: return "Keep practicing";',
          },
        ],
      },
      {
        id: "practice-refactor-branches",
        title: "Debug: The Dead Branch",
        prompt: `This classifier has a bug: the second branch can never run. Reorder or fix the conditions so each score range reports correctly — under 60 \`"cold"\`, 60–79 \`"warm"\`, 80+ \`"hot"\` for \`function temp(score)\`.

Rules:
- All three results reachable.
- Keep it as chained if / else if / else.`,
        difficulty: "beginner",
        boilerplate: `function temp(score) {
  if (score >= 60) {
    return "warm";
  } else if (score >= 80) {
    return "hot";
  } else {
    return "cold";
  }
}
console.log(temp(85));
`,
        tests: [
          {
            name: "all three ranges reachable",
            code: `const fn = new Function(code + "\\nreturn temp;");
const t = fn();
const out = new Set([t(85), t(70), t(30)]);
if (!out.has("hot")) throw new Error("85 must return 'hot' — it currently can't.");
if (t(70) !== "warm") throw new Error("70 must return 'warm'.");
if (t(30) !== "cold") throw new Error("30 must return 'cold'.");`,
            hint: "Check the highest threshold FIRST: 80+ hot, then 60+ warm, else cold.",
          },
          {
            name: "still chained conditionals",
            code: `if (!/else\\s+if/i.test(code)) {
  throw new Error("Keep the if / else if / else chain — reordering, not rewriting.");
}`,
            hint: "Fix the order of the conditions; the structure stays a chain.",
          },
        ],
      },
    ],
  },
  {
    file: "js-loops-practice.json",
    id: "js-loops-practice",
    title: "Repetition Without Repetition",
    description:
      "Loops that do real work: a countdown, a running total, and building a string across iterations.",
    afterLesson: "js-loops",
    minutes: 12,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-countdown-loop",
        title: "Countdown and Total",
        prompt: `Write \`function sumUpTo(n)\` that returns 1 + 2 + … + n using a loop — no hard-coded totals. Log \`sumUpTo(10)\` (should be 55) and \`sumUpTo(100)\`.

Rules:
- A \`for\` (or \`while\`) loop accumulates the sum.
- Works for any n, not just 10.`,
        difficulty: "beginner",
        boilerplate:
          "function sumUpTo(n) {\n  // loop and accumulate\n}\nconsole.log(sumUpTo(10));\nconsole.log(sumUpTo(100));\n",
        tests: [
          {
            name: "sums 1..10 to 55",
            code: `const fn = new Function(code + "\\nreturn sumUpTo;");
if (fn()(10) !== 55) throw new Error("sumUpTo(10) should be 55.");`,
            hint: "Start a total at 0, add each i from 1 to n, then return it.",
          },
          {
            name: "works for other inputs",
            code: `const fn = new Function(code + "\\nreturn sumUpTo;");
if (fn()(100) !== 5050) throw new Error("sumUpTo(100) should be 5050.");
if (fn()(1) !== 1) throw new Error("sumUpTo(1) should be 1.");`,
            hint: "The loop bound must come from the parameter n — then any input works.",
          },
          {
            name: "no hard-coded result",
            code: `const body = code.match(/function\\s+sumUpTo[\\s\\S]*\\}/)[0];
if (!/for|while/.test(body)) throw new Error("Use a for or while loop inside sumUpTo.");
if (/\\b55\\b|\\b5050\\b/.test(body)) throw new Error("No hard-coded totals — the loop computes the answer.");`,
            hint: "The function body needs a real loop and no magic numbers.",
          },
        ],
      },
      {
        id: "practice-loop-string-builder",
        title: "Build a String Across Iterations",
        prompt: `Write \`function stars(rows)\` that returns a string with one line per row, each line containing row-count \`*\` characters followed by \`\\n\`. \`stars(3)\` returns \`"**\\n***\\n***\\n"\`… wait — check the example: \`stars(3)\` is line 1: \`*\`, line 2: \`**\`, line 3: \`***\`, each ending with \`\\n\`.

Rules:
- Accumulate into one string and return it.
- Line k has k stars.`,
        difficulty: "beginner",
        boilerplate:
          "function stars(rows) {\n  // accumulate lines\n}\nconsole.log(JSON.stringify(stars(3)));\n",
        tests: [
          {
            name: "three rows produce a growing triangle",
            code: `const fn = new Function(code + "\\nreturn stars;");
const out = fn()(3);
if (out !== "*\\n**\\n***\\n") throw new Error("stars(3) should be '*\\n**\\n***\\n' — line k has k stars, each line ends with \\n.");`,
            hint: "Line 1: one star. Line 2: two. Line 3: three. Every line ends with a newline.",
          },
          {
            name: "handles other sizes",
            code: `const fn = new Function(code + "\\nreturn stars;");
if (fn()(1) !== "*\\n") throw new Error("stars(1) is '*\\n'.");
if (fn()(0) !== "") throw new Error("stars(0) is an empty string.");`,
            hint: "Zero rows → empty string. Your loop just never runs.",
          },
          {
            name: "returns, not logs",
            code: `const body = code.match(/function\\s+stars[\\s\\S]*\\n\\}/)[0];
if (!/return/.test(body)) throw new Error("stars must return the string, not just log it.");`,
            hint: "Build the string in a variable and return it at the end.",
          },
        ],
      },
    ],
  },
  {
    file: "js-functions-practice.json",
    id: "js-functions-practice",
    title: "Functions That Earn Their Name",
    description:
      "Parameters, returns, and reuse: a converter, a comparator, and turning repeated code into one function with a default value.",
    afterLesson: "js-functions",
    minutes: 14,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-converter-function",
        title: "Build a Temperature Converter",
        prompt: `Write \`function celsiusToFahrenheit(c)\` that returns \`c * 9 / 5 + 32\`. Log the results for 0, 100, and 37.

Rules:
- One function, three calls with different arguments.`,
        difficulty: "beginner",
        boilerplate:
          "function celsiusToFahrenheit(c) {\n  // convert and return\n}\n// log 0, 100, and 37\n",
        tests: [
          {
            name: "converts correctly",
            code: `const fn = new Function(code + "\\nreturn celsiusToFahrenheit;");
const f = fn();
if (f(0) !== 32) throw new Error("0°C should be 32°F.");
if (f(100) !== 212) throw new Error("100°C should be 212°F.");
if (f(37) !== 98.6) throw new Error("37°C should be 98.6°F.");`,
            hint: "return c * 9 / 5 + 32; — multiplication and division before the addition.",
          },
          {
            name: "three calls logged",
            code: `const calls = (code.match(/celsiusToFahrenheit\\s*\\(\\s*[\\d.]+\\s*\\)/g) ?? []).length;
if (calls < 3) throw new Error("Call the function with 0, 100, and 37.");`,
            hint: "console.log(celsiusToFahrenheit(0)); and two more.",
          },
        ],
      },
      {
        id: "practice-default-parameter",
        title: "A Sensible Default",
        prompt: `Write \`function greet(name, greeting = "Hello")\` that returns \`\${greeting}, \${name}!\`. \`greet("Ada")\` returns \`Hello, Ada!\`; \`greet("Ada", "Bonjour")\` returns \`Bonjour, Ada!\`.

Rules:
- The second parameter has a default value — no if-check.`,
        difficulty: "beginner",
        boilerplate:
          'function greet(name, greeting) {\n  // use a default parameter\n}\nconsole.log(greet("Ada"));\nconsole.log(greet("Ada", "Bonjour"));\n',
        tests: [
          {
            name: "default kicks in",
            code: `const fn = new Function(code + "\\nreturn greet;");
if (fn()("Ada") !== "Hello, Ada!") throw new Error("greet('Ada') should be 'Hello, Ada!'.");`,
            hint: 'function greet(name, greeting = "Hello") — the default fills in when the argument is missing.',
          },
          {
            name: "override works",
            code: `const fn = new Function(code + "\\nreturn greet;");
if (fn()("Ada", "Bonjour") !== "Bonjour, Ada!") throw new Error("greet('Ada', 'Bonjour') should be 'Bonjour, Ada!'.");`,
            hint: "A passed argument replaces the default.",
          },
          {
            name: "default in the signature, not an if",
            code: `const sig = code.match(/function\\s+greet\\s*\\(([^)]*)\\)/)[1];
if (!/=/i.test(sig)) throw new Error("Put the default in the parameter list: greeting = \\"Hello\\".");
if (/if\\s*\\([^)]*greeting/i.test(code)) throw new Error("No if needed — the default parameter handles it.");`,
            hint: "The = goes right in the signature. No branching required.",
          },
        ],
      },
    ],
  },
  {
    file: "js-arrays-practice.json",
    id: "js-arrays-practice",
    title: "Array Workouts",
    description:
      "Real data-crunching: filter passing scores, map to new values, find one item — the three moves behind most array work.",
    afterLesson: "js-arrays",
    minutes: 14,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-filter-scores",
        title: "Filter the Passing Scores",
        prompt: `Given \`const scores = [45, 92, 67, 88, 30]\`, produce \`passing\` — a new array of only the scores ≥ 60 — using \`.filter()\`. Log how many passed.

Rules:
- Use \`.filter()\`; don't mutate \`scores\`.`,
        difficulty: "beginner",
        boilerplate: "const scores = [45, 92, 67, 88, 30];\n// filter, then log the count\n",
        tests: [
          {
            name: "filter with a threshold test",
            code: `if (!/\\.filter\\s*\\(/.test(code)) throw new Error("Use .filter() to build the passing array.");
if (/scores\\s*=\\s*[^=]/.test(code.replace(/const\\s+scores\\s*=\\s*\\[[^\\]]*\\]\\s*;?/, ""))) {
  throw new Error("Don't reassign scores — filter returns a NEW array.");
}`,
            hint: "const passing = scores.filter((s) => s >= 60);",
          },
          {
            name: "the right scores survive",
            code: `const fn = new Function(code + "\\nreturn typeof passing !== 'undefined' ? passing : null;");
const p = fn();
if (!p || p.join(",") !== "92,67,88") throw new Error("passing should be [92, 67, 88].");`,
            hint: "45 and 30 are below 60 — they should not survive the filter.",
          },
          {
            name: "count is logged",
            code: `if (!/console\\.log\\([^)]*(passing\\.length|\\.length)/.test(code)) {
  throw new Error("Log how many passed — passing.length.");
}`,
            hint: "console.log(passing.length);",
          },
        ],
      },
      {
        id: "practice-map-transform",
        title: "Transform Every Item",
        prompt: `Given \`const prices = [10, 20, 30]\`, use \`.map()\` to build \`withTax\` — every price with 20% tax added (so [12, 24, 36]). Log the new array.

Rules:
- \`.map()\` returns a new array; original untouched.`,
        difficulty: "beginner",
        boilerplate: "const prices = [10, 20, 30];\n// map with 20% tax, then log\n",
        tests: [
          {
            name: "map produces the taxed prices",
            code: `const fn = new Function(code + "\\nreturn withTax;");
const w = fn();
if (!w || w.join(",") !== "12,24,36") throw new Error("withTax should be [12, 24, 36].");`,
            hint: "const withTax = prices.map((p) => p * 1.2); — careful with floating point: use p * 1.2 and check loosely if needed.",
          },
          {
            name: "original array untouched",
            code: `const fn = new Function(code + "\\nreturn prices;");
if (fn().join(",") !== "10,20,30") throw new Error("prices must stay [10, 20, 30] — map never mutates.");`,
            hint: "If your result is right but prices changed, you mutated instead of mapping.",
          },
        ],
      },
      {
        id: "practice-find-one",
        title: "Find the One That Matters",
        prompt: `Given \`const users = [{ name: "Ada", admin: false }, { name: "Grace", admin: true }, { name: "Linus", admin: false }]\`, use \`.find()\` to get the first admin and log their name (should be \`Grace\`).

Rules:
- \`.find()\` with a condition on \`admin\`.`,
        difficulty: "beginner",
        boilerplate:
          'const users = [{ name: "Ada", admin: false }, { name: "Grace", admin: true }, { name: "Linus", admin: false }];\n// find the first admin and log the name\n',
        tests: [
          {
            name: "find with the admin condition",
            code: `if (!/\\.find\\s*\\(/.test(code)) throw new Error("Use .find() — it stops at the first match.");`,
            hint: "users.find((u) => u.admin) — truthy admin property.",
          },
          {
            name: "logs Grace",
            code: `const fn = new Function(code + "\\nreturn null;");
let logged = "";
const fakeConsole = { log: (...a) => { logged += a.join(" "); } };
const sandboxCode = code.replace(/console\\.log/g, "fakeConsole.log");
new Function("fakeConsole", sandboxCode)(fakeConsole);
if (!logged.includes("Grace")) throw new Error("The log should output Grace.");`,
            hint: "console.log(users.find((u) => u.admin).name);",
          },
        ],
      },
    ],
  },
];

const REFS = {
  "practice-const-vs-let": `const firstName = "Ada";
let score = 0;
score = 42;
console.log(\`\${firstName}: \${score}\`);`,
  "practice-shopping-total": `const price = 4.5;
const quantity = 3;
const total = price * quantity;
console.log(\`\${quantity} items cost \${total}\`);
console.log(total > 10);`,
  "practice-grade-gates": `function grade(score) {
  if (score >= 90) return "A";
  else if (score >= 80) return "B";
  else return "Keep practicing";
}
console.log(grade(92));
console.log(grade(55));`,
  "practice-refactor-branches": `function temp(score) {
  if (score >= 80) {
    return "hot";
  } else if (score >= 60) {
    return "warm";
  } else {
    return "cold";
  }
}
console.log(temp(85));`,
  "practice-countdown-loop": `function sumUpTo(n) {
  let total = 0;
  for (let i = 1; i <= n; i++) {
    total += i;
  }
  return total;
}
console.log(sumUpTo(10));
console.log(sumUpTo(100));`,
  "practice-loop-string-builder": `function stars(rows) {
  let out = "";
  for (let i = 1; i <= rows; i++) {
    out += "*".repeat(i) + "\\n";
  }
  return out;
}
console.log(JSON.stringify(stars(3)));`,
  "practice-converter-function": `function celsiusToFahrenheit(c) {
  return (c * 9) / 5 + 32;
}
console.log(celsiusToFahrenheit(0));
console.log(celsiusToFahrenheit(100));
console.log(celsiusToFahrenheit(37));`,
  "practice-default-parameter": `function greet(name, greeting = "Hello") {
  return \`\${greeting}, \${name}!\`;
}
console.log(greet("Ada"));
console.log(greet("Ada", "Bonjour"));`,
  "practice-filter-scores": `const scores = [45, 92, 67, 88, 30];
const passing = scores.filter((s) => s >= 60);
console.log(passing.length);`,
  "practice-map-transform": `const prices = [10, 20, 30];
const withTax = prices.map((p) => Math.round(p * 1.2));
console.log(withTax);`,
  "practice-find-one": `const users = [{ name: "Ada", admin: false }, { name: "Grace", admin: true }, { name: "Linus", admin: false }];
console.log(users.find((u) => u.admin).name);`,
};

const WRONGL = {
  "practice-const-vs-let": `var firstName = "Ada";
var score = 0;`,
  "practice-shopping-total": "const total = 13.5;",
  "practice-grade-gates": 'function grade(score) { return "A"; }',
  "practice-refactor-branches": `function temp(score) { if (score >= 60) { return "warm"; } else if (score >= 80) { return "hot"; } else { return "cold"; } }`,
  "practice-countdown-loop": "function sumUpTo(n) { return 55; }",
  "practice-loop-string-builder": 'function stars(rows) { return "*\\n"; }',
  "practice-converter-function": "function celsiusToFahrenheit(c) { return c + 32; }",
  "practice-default-parameter": `function greet(name, greeting) { if (greeting === undefined) { greeting = "Hi"; } return greeting + ", " + name + "!"; }`,
  "practice-filter-scores": "const passing = scores;",
  "practice-map-transform": "const withTax = prices.push(36);",
  "practice-find-one": 'console.log("Grace");',
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
