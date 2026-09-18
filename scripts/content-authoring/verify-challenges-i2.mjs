/**
 * Challenge QA harness — INTERMEDIATE course.
 * Same execution engine as verify-challenges.mjs (beginner); walks the
 * intermediate course and uses scripts/content-authoring/i2-solutions.mjs.
 * Run: node scripts/content-authoring/verify-challenges-i2.mjs
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const TRACK = "src/content/tracks/web-development/courses/web-development-intermediate/modules";

/** Mirrors buildTestFile(): author snippet inside try/catch with `code` bound. */
function runTestSnippet(testCode, studentCode, sandboxArgs) {
  const sandbox = {
    code: studentCode,
    console: { log: () => {}, error: () => {}, warn: () => {} },
    result: undefined,
    // REAL timers — async test snippets rely on genuine scheduling.
    setTimeout,
    clearTimeout,
    AbortController,
    URLSearchParams,
    URL,
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
  const DOM_CHALLENGES = []; // extended when DOM challenges are authored
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

// ── Default wrong solution (should fail any non-trivial test) ──
const WRONG_DEFAULT = "";

const R = {};
const W = {};
import { R as I2_R, W as I2_W } from "./i2-solutions.mjs";
Object.assign(R, I2_R);
Object.assign(W, I2_W);
let passCount = 0;
let failCount = 0;
const failures = [];

const modules = readdirSync(TRACK);
for (const mod of modules) {
  // ── Lesson-attached challenges (checkpoints only since the revision) ──
  const lessonsDir = path.join(TRACK, mod, "lessons");
  const entries = readdirSync(lessonsDir);
  for (const entry of entries) {
    if (!entry.endsWith(".json") || entry.endsWith(".vi.json")) continue; // skip vi sidecars
    const lesson = JSON.parse(readFileSync(path.join(lessonsDir, entry), "utf8"));
    const chDir = path.join(lessonsDir, lesson.id, "challenges");
    let challengeFiles = [];
    try {
      challengeFiles = readdirSync(chDir).filter(
        (f) => f.endsWith(".json") && !f.endsWith(".vi.json"),
      );
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

  // ── Practice-set challenges (the main coding layer since the revision) ──
  const practicesDir = path.join(TRACK, mod, "practices");
  let practiceEntries = [];
  try {
    practiceEntries = readdirSync(practicesDir).filter(
      (f) => f.endsWith(".json") && !f.endsWith(".vi.json"),
    );
  } catch {
    practiceEntries = []; // module has no practices
  }
  for (const pf of practiceEntries) {
    const setManifest = JSON.parse(readFileSync(path.join(practicesDir, pf), "utf8"));
    for (const challengeId of setManifest.challenges) {
      const chFile = path.join(practicesDir, setManifest.id, "challenges", `${challengeId}.json`);
      if (!existsSync(chFile)) {
        failCount++;
        failures.push(challengeId);
        console.log(`  FAIL ${challengeId} — challenge file missing (${chFile})`);
        continue;
      }
      const challenge = JSON.parse(readFileSync(chFile, "utf8"));
      const ref = R[challenge.id] ?? R[challengeId];
      const wrong = W[challenge.id] ?? WRONG_DEFAULT;
      if (ref === undefined) {
        failCount++;
        failures.push(challenge.id);
        console.log(`  FAIL ${challenge.id} — no reference solution in harness`);
        continue;
      }

      const refResults = await runChallengeTests(challenge, ref, buildStubs(challenge.id));
      const refOk = refResults.every((r) => r.result === "PASS");
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
