/**
 * Challenge QA harness — AP CSA ADVANCED (two-sided).
 *
 * For every challenge: the reference solution (R) must make all tests pass,
 * the intentionally-wrong solution (W) must fail at least one test.
 *
 * Uses buildJavaTestFile() from src/workers/java-runtime.ts so the QA test
 * files are byte-identical to what the sandbox compiles (no drift), then
 * compiles and runs each test the same way the sandbox does
 * (`javac --release 21`, `java Test_x`, exit status).
 *
 * Optional argv[2] = challenge-id filter (substring match) for fast scoped
 * re-runs during authoring; without it, the whole course is verified.
 *
 * Run: node --import tsx --import ./scripts/worker-imports.mjs \
 *        scripts/content-authoring/verify-challenges-apx.mjs [id-filter]
 */
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildJavaTestFile, javaSanitizeName, JAVA_RELEASE_ARGS } from "../../src/workers/java-runtime.ts";

const COURSE = path.resolve("src/content/tracks/ap-csa/courses/ap-csa-advanced");
const { R, W } = await import("./apx-solutions.mjs");
const FILTER = process.argv[2] || null;

// ---------- load every challenge (practice sets + checkpoint lessons) ----------
const challenges = new Map(); // id -> {data, jsonPath}

function addChallengeFile(p) {
  if (!p.endsWith(".json") || p.endsWith(".vi.json")) return;
  const d = JSON.parse(readFileSync(p, "utf8"));
  if (d && d.id && Array.isArray(d.tests)) {
    challenges.set(d.id, { data: d, jsonPath: p });
  }
}

const modulesDir = path.join(COURSE, "modules");
for (const mod of readdirSync(modulesDir)) {
  const modDir = path.join(modulesDir, mod);
  // practice-set challenges
  const practicesDir = path.join(modDir, "practices");
  try {
    for (const sid of readdirSync(practicesDir)) {
      const chDir = path.join(practicesDir, sid, "challenges");
      try {
        for (const f of readdirSync(chDir)) addChallengeFile(path.join(chDir, f));
      } catch {}
    }
  } catch {}
  // checkpoint-lesson challenges
  const lessonsDir = path.join(modDir, "lessons");
  try {
    for (const lid of readdirSync(lessonsDir)) {
      const chDir = path.join(lessonsDir, lid, "challenges");
      try {
        for (const f of readdirSync(chDir)) addChallengeFile(path.join(chDir, f));
      } catch {}
    }
  } catch {}
}

// ---------- compile + run helpers (mirror the sandbox job) ----------
const work = mkdtempSync(path.join(os.tmpdir(), "apx-qa-"));
const classesDir = path.join(work, "classes");
let pass = 0;
let verified = 0;
const failures = [];

function verifyCase(id, key, expectPass) {
  const ch = challenges.get(id);
  const sol = key === "R" ? R[id] : W[id];
  if (!sol || typeof sol !== "string") {
    failures.push(`${id}: missing ${key} solution in ledger`);
    return { failedTests: 1, total: 0 };
  }
  writeFileSync(path.join(work, "Solution.java"), sol);
  const results = [];
  for (const test of ch.data.tests) {
    const name = javaSanitizeName(test.name);
    const testPath = path.join(work, `Test_${name}.java`);
    writeFileSync(testPath, buildJavaTestFile(test));
    const cc = spawnSync(
      "javac",
      [...JAVA_RELEASE_ARGS, "-nowarn", "-d", classesDir, path.join(work, "Solution.java"), testPath],
      { timeout: 60_000, encoding: "utf8" },
    );
    if (cc.status !== 0) {
      results.push({ name, ok: false, phase: "compile", log: cc.stderr });
      continue;
    }
    const run = spawnSync(
      "java",
      ["-XX:+UseSerialGC", "-Xss4m", "-cp", classesDir, `Test_${name}`],
      { timeout: 15_000, encoding: "utf8" },
    );
    results.push({ name, ok: run.status === 0, phase: "run", log: run.stderr });
  }
  const failedTests = results.filter((r) => !r.ok);
  const passedAll = results.length > 0 && failedTests.length === 0;
  if (expectPass && !passedAll) {
    failures.push(
      `${id} [${key}] REFERENCE MUST PASS but failed ${failedTests.length}/${results.length}: ` +
        failedTests
          .map((f) => `${f.name} (${f.phase}): ${(f.log || "").split("\n").find((l) => l.trim())?.slice(0, 160) ?? "?"}`)
          .join(" | "),
    );
  }
  if (!expectPass && passedAll) {
    failures.push(`${id} [${key}] WRONG SOLUTION MUST FAIL but all ${results.length} tests passed`);
  }
  return { failedTests: failedTests.length, total: results.length };
}

// ---------- main ----------
console.log(`challenges on disk: ${challenges.size}`);
for (const id of [...challenges.keys()].sort()) {
  if (FILTER && !id.includes(FILTER)) continue;
  const r = verifyCase(id, "R", true);
  const w = verifyCase(id, "W", false);
  verified++;
  const ok = r.failedTests === 0 && w.failedTests > 0;
  if (ok) pass++;
  console.log(`${ok ? "OK " : "FAIL"} ${id} (R ${r.failedTests}/${r.total} fail, W ${w.failedTests}/${w.total} fail)`);
}

rmSync(work, { recursive: true, force: true });
console.log(`\nverified: ${pass}/${verified} challenges two-sided OK`);
if (failures.length) {
  console.log(`\n${failures.length} FAILURES:`);
  for (const f of failures) console.log("  - " + f);
  process.exit(1);
}
