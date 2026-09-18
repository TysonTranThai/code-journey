/**
 * Challenge QA harness — ADVANCED course (Course 3, Advanced HTML section).
 * Same execution engine as verify-challenges.mjs / verify-challenges-i2.mjs;
 * walks the advanced course and uses scripts/content-authoring/c3-solutions.mjs.
 * Run: node scripts/content-authoring/verify-challenges-c3.mjs
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { REFERENCE_SOLUTIONS, WRONG_SOLUTIONS } from "./c3-solutions.mjs";

const TRACK = "src/content/tracks/web-development/courses/web-development-advanced/modules";

/** Mirrors the platform's buildTestFile(): author snippet inside try/catch, `code` bound. */
function runTestSnippet(testCode, studentCode) {
  const sandbox = {
    code: studentCode,
    console: { log: () => {}, error: () => {}, warn: () => {} },
    result: undefined,
  };
  const context = vm.createContext(sandbox);
  const script = new vm.Script(
    `(function () { try { ${testCode}\n result = "PASS"; } catch (err) { result = "FAIL: " + (err && err.message ? err.message : String(err)); } })()`,
  );
  script.runInContext(context);
  return sandbox.result;
}

async function runChallengeTests(challenge, solution) {
  const results = [];
  for (const t of challenge.tests) {
    const r = runTestSnippet(t.code, solution);
    results.push({ name: t.name, result: r });
  }
  return results;
}

function* walkChallenges() {
  for (const moduleId of readdirSync(TRACK)) {
    const modDir = path.join(TRACK, moduleId);
    const practicesDir = path.join(modDir, "practices");
    if (!existsSync(practicesDir)) continue;
    for (const entry of readdirSync(practicesDir)) {
      if (!entry.endsWith(".json") || entry.endsWith(".vi.json")) continue;
      const setId = entry.replace(/\.json$/, "");
      const setJson = JSON.parse(readFileSync(path.join(practicesDir, entry), "utf8"));
      const chDir = path.join(practicesDir, setId, "challenges");
      if (!existsSync(chDir)) continue;
      for (const c of readdirSync(chDir)) {
        if (!c.endsWith(".json") || c.endsWith(".vi.json")) continue;
        const ch = JSON.parse(readFileSync(path.join(chDir, c), "utf8"));
        if (!setJson.challenges.includes(ch.id)) {
          console.log(`  WARN ${ch.id}: not declared in ${setId}`);
        }
        yield ch;
      }
    }
  }
}

let passed = 0;
let failed = 0;
const failures = [];

for (const challenge of walkChallenges()) {
  const ref = REFERENCE_SOLUTIONS[challenge.id];
  const wrong = WRONG_SOLUTIONS[challenge.id];
  if (!ref || !wrong) {
    failed++;
    failures.push(`${challenge.id}: missing ${!ref ? "reference" : "wrong"} solution in c3-solutions.mjs`);
    continue;
  }
  const refResults = await runChallengeTests(challenge, ref);
  const refBad = refResults.filter((r) => r.result !== "PASS");
  const wrongResults = await runChallengeTests(challenge, wrong);
  const wrongBlocked = wrongResults.some((r) => r.result !== "PASS");
  if (refBad.length === 0 && wrongBlocked) {
    passed++;
    console.log(`  OK  ${challenge.id}`);
  } else {
    failed++;
    console.log(`  FAIL ${challenge.id}`);
    for (const r of refBad) {
      console.log(`    ref fails: ${r.name} → ${r.result}`);
    }
    if (!wrongBlocked) {
      console.log(`    wrong solution PASSED all tests (grading loophole)`);
    }
    failures.push(challenge.id);
  }
}

console.log(`\n${passed} challenges verified, ${failed} failed`);
if (failures.length > 0) {
  console.log("Failures:", failures.join(", "));
  process.exit(1);
}
