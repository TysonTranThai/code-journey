/**
 * Challenge QA harness — C++ INTERMEDIATE (two-sided).
 *
 * For every challenge: the reference solution (R) must make all tests pass,
 * the intentionally-wrong solution (W) must fail at least one test.
 *
 * Uses buildCppTestFile() from src/workers/cpp-runtime.ts so the QA test
 * files are byte-identical to what the sandbox compiles (no drift), then
 * compiles and runs each test the same way the sandbox does
 * (`g++ -std=c++20 -Wall -Wextra -Wpedantic`, run, exit status).
 *
 * Run: node --import tsx --import ./scripts/worker-imports.mjs \
 *        scripts/content-authoring/verify-challenges-cppi.mjs
 */
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildCppTestFile, cppSanitizeName } from "../../src/workers/cpp-runtime.ts";

const COURSE = path.resolve("src/content/tracks/cpp/courses/cpp-intermediate");
const { R, W } = await import("./cpp-intermediate-solutions.mjs");

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

// ---------- compile + run helpers (mirror the sandbox job) ----------
const work = mkdtempSync(path.join(os.tmpdir(), "cj-cppi-qa-"));
let pass = 0;
const failures = [];

function compileTest(id, test) {
  const name = cppSanitizeName(test.name);
  const src = path.join(work, `${id}-${name}.cpp`);
  const bin = path.join(work, `${id}-${name}.bin`);
  const unit = buildCppTestFile(test);
  // solution.cpp sits in the same work dir, so #include "solution.cpp" resolves.
  return { name, src, bin, unit };
}

async function verifyCase(id, key, expectPass) {
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
console.log(`challenges on disk: ${challenges.size}`);
let verified = 0;
for (const id of [...challenges.keys()].sort()) {
  const r = await verifyCase(id, "R", true);
  const w = await verifyCase(id, "W", false);
  verified++;
  const mark = r.passedAll && !w.passedAll ? "OK " : "FAIL";
  if (mark === "OK ") pass++;
  console.log(`${mark} ${id} (R ${r.failedTests.length}/${r.total} fail, W ${w.failedTests.length}/${w.total} fail)`);
}

rmSync(work, { recursive: true, force: true });
console.log(`\nverified: ${pass}/${verified} challenges two-sided OK`);
if (failures.length) {
  console.log(`\n${failures.length} FAILURES:`);
  for (const f of failures) console.log("  - " + f);
  process.exit(1);
}
