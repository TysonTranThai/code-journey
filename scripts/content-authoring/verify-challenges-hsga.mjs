/**
 * Challenge QA harness — HSG ADVANCED (two-sided).
 *
 * For every challenge: the reference solution (R) must make all tests pass,
 * the intentionally-wrong solution (W) must fail at least one test.
 *
 * Uses buildCppTestFile() from src/workers/cpp-runtime.ts so the QA test
 * files are byte-identical to what the sandbox compiles (no drift), then
 * compiles and runs each test the same way the sandbox does
 * (`g++ -std=c++20 -Wall -Wextra -Wpedantic`, run, exit status).
 *
 * Run: npx tsx scripts/content-authoring/verify-challenges-hsg.mjs [id-filter]
 */
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildCppTestFile, cppSanitizeName } from "../../src/workers/cpp-runtime.ts";

const COURSE = path.resolve("src/content/tracks/hsg/courses/hsg-advanced");
const SOLUTIONS = process.argv[3] ?? "./hsg-advanced-solutions.mjs";
const { R, W } = await import(SOLUTIONS);

// ---------- load every challenge (practice sets + checkpoint lessons) ----------
const challenges = new Map(); // id -> {data, jsonPath}

function addChallengeFile(p) {
  if (!p.endsWith(".json") || p.endsWith(".vi.json")) return;
  const d = JSON.parse(readFileSync(p, "utf8"));
  if (d && d.id && Array.isArray(d.tests)) {
    challenges.set(d.id, { data: d, jsonPath: p });
  }
}

for (const mod of readdirSync(path.join(COURSE, "modules"))) {
  const modDir = path.join(COURSE, "modules", mod);
  const practicesDir = path.join(modDir, "practices");
  try {
    for (const sid of readdirSync(practicesDir)) {
      const chDir = path.join(practicesDir, sid, "challenges");
      try {
        for (const f of readdirSync(chDir)) addChallengeFile(path.join(chDir, f));
      } catch {}
    }
  } catch {}
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

const only = process.argv[2] ?? "";
const selected = [...challenges.entries()].filter(([id]) => !only || id.includes(only));
console.log("challenges:", selected.length, only ? `(filter: ${only})` : "");

// ---------- compile + run helpers (mirror the sandbox job) ----------
const work = mkdtempSync(path.join(os.tmpdir(), "cj-hsg-qa-"));
let pass = 0;
const failures = [];
let rPass = 0, rFail = 0, wPass = 0, wFail = 0;

function compileTest(id, test) {
  const name = cppSanitizeName(test.name);
  const src = path.join(work, `${id}-${name}.cpp`);
  const bin = path.join(work, `${id}-${name}.bin`);
  const unit = buildCppTestFile(test);
  return { name, src, bin, unit };
}

function verifyCase(id, key, expectPass) {
  const ch = challenges.get(id);
  const sol = key === "R" ? R[id] : W[id];
  if (!sol || typeof sol !== "string") {
    failures.push(`${id}: missing ${key} solution in ledger`);
    return { passedAll: false, failedTests: [], total: 0 };
  }
  writeFileSync(path.join(work, "solution.cpp"), sol);
  const results = [];
  for (const test of ch.data.tests) {
    const { name, src, bin, unit } = compileTest(id, test);
    writeFileSync(src, unit);
    const cc = spawnSync(
      "g++",
      ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-o", bin, src],
      { timeout: 60_000, encoding: "utf8" },
    );
    if (cc.status !== 0) {
      results.push({ name, ok: false, phase: "compile", log: cc.stderr });
      continue;
    }
    const run = spawnSync(bin, { timeout: 15_000, encoding: "utf8" });
    results.push({ name, ok: run.status === 0, phase: "run", log: run.stderr });
  }
  const failedTests = results.filter((r) => !r.ok);
  const passedAll = results.length > 0 && failedTests.length === 0;
  for (const r of results) {
    if (key === "R") r.ok ? rPass++ : rFail++;
    else r.ok ? wPass++ : wFail++;
  }
  if (expectPass && !passedAll) {
    failures.push(
      `${id} [${key}] REFERENCE MUST PASS but failed ${failedTests.length}/${results.length}: ` +
        failedTests
          .map((f) => `${f.name} (${f.phase}): ${(f.log || "").split("\n")[0].slice(0, 160)}`)
          .join(" | "),
    );
  }
  if (!expectPass && passedAll) {
    failures.push(`${id} [${key}] WRONG SOLUTION MUST FAIL but all ${results.length} tests passed`);
  }
  return { passedAll, failedTests, total: results.length };
}

// ---------- main ----------
let verified = 0;
for (const [id] of selected) {
  const r = verifyCase(id, "R", true);
  const w = verifyCase(id, "W", false);
  verified++;
  const mark = r.passedAll && !w.passedAll ? "clean" : "FAIL";
  if (mark === "clean") pass++;
  console.log(`${mark} ${id} (R ${r.failedTests.length}/${r.total} fail, W ${w.failedTests.length}/${w.total} fail)`);
}

rmSync(work, { recursive: true, force: true });
console.log(`\nR tests: ${rPass} pass / ${rFail} fail   W tests: ${wFail} fail / ${wPass} pass`);
console.log(`challenge verdicts: ${pass} clean, ${verified - pass} not-clean`);
if (failures.length) {
  console.log(`\n${failures.length} FAILURES:`);
  for (const f of failures) console.log("  - " + f);
  process.exit(1);
}
