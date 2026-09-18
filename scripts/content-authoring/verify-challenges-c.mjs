/**
 * Challenge QA harness — C BEGINNER (two-sided, batched sandbox execution).
 *
 * For every challenge: the reference solution (R) must make all tests pass,
 * the intentionally-wrong solution (W) must fail at least one test.
 *
 * Uses buildCTestFile() from src/workers/c-runtime.ts so the QA test files
 * are byte-identical to what the sandbox compiles (no drift), then compiles
 * and runs each test with the REAL sandbox image (`gcc -std=c23 -Wall
 * -Wextra -Wpedantic`) in ONE batched container pass (per-test docker spawns
 * would be ~1200 container launches — minutes per test).
 *
 * Run: node --import tsx --import ./scripts/worker-imports.mjs \
 *        scripts/content-authoring/verify-challenges-c.mjs
 */
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import {
  buildCTestFile,
  cSanitizeName,
  C_STANDARD_FLAG,
  C_TEST_WARNING_FLAGS,
} from "../../src/workers/c-runtime.ts";

const COURSE = path.resolve("src/content/tracks/c/courses/c-beginner");
const { R, W } = await import("./cb-solutions.mjs");

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

const only = process.env.CB_ONLY ?? "";
const selected = [...challenges.entries()].filter(([id]) => !only || id.includes(only));
console.log(`challenges on disk: ${challenges.size}${only ? ` (filter: ${only})` : ""}`);

// ---------- Phase 1: stage solutions + byte-identical test files ----------
const stage = mkdtempSync(path.join(os.tmpdir(), "cj-c-qa-"));
const jobs = [];
const missing = [];
for (const [id, { data }] of selected) {
  const solSrc = R[id] ?? null;
  const wrongSrc = W[id] ?? null;
  if (typeof solSrc !== "string") {
    missing.push(`${id}: missing R solution in ledger`);
    continue;
  }
  if (typeof wrongSrc !== "string") {
    missing.push(`${id}: missing W solution in ledger`);
    continue;
  }
  writeFileSync(path.join(stage, `sol-${id}.c`), solSrc);
  writeFileSync(path.join(stage, `wrong-${id}.c`), wrongSrc);
  const testNames = data.tests.map((t) => cSanitizeName(t.name));
  data.tests.forEach((t, i) => {
    writeFileSync(path.join(stage, `test-${id}-${testNames[i]}.c`), buildCTestFile(t));
  });
  jobs.push({ id, tests: testNames });
}
if (missing.length) {
  console.error("MISSING LEDGER ENTRIES:\n  " + missing.join("\n  "));
  rmSync(stage, { recursive: true, force: true });
  process.exit(1);
}

// ---------- Phase 2: one batched container pass with the real sandbox gcc ----------
const lines = ["set -u", "cd /work"];
for (const job of jobs) {
  for (const [variant, file] of [
    ["sol", `sol-${job.id}.c`],
    ["wrong", `wrong-${job.id}.c`],
  ]) {
    lines.push(`cp "${file}" solution.c`);
    for (const name of job.tests) {
      const bin = `b-${variant}-${job.id}-${name}`;
      lines.push(
        `gcc ${C_STANDARD_FLAG} ${C_TEST_WARNING_FLAGS} -o "/tmp/${bin}" "test-${job.id}-${name}.c" -lm 2> "err-${bin}.log"`,
      );
      lines.push(`if [ $? -ne 0 ]; then echo "RESULT ${variant} ${job.id} ${name} BUILD_FAIL"; continue; fi`);
      lines.push(`"/tmp/${bin}" > "out-${bin}.log" 2> "hint-${bin}.log"`);
      lines.push(`echo "RESULT ${variant} ${job.id} ${name} status=$?"`);
    }
  }
}
writeFileSync(path.join(stage, "run.sh"), lines.join("\n") + "\n");

const r = spawnSync(
  "docker",
  ["run", "--rm", "--network", "none", "-v", `${stage}:/work`, "-w", "/work", "codejourney-sandbox:latest", "sh", "run.sh"],
  { encoding: "utf8", timeout: 600_000, maxBuffer: 64 * 1024 * 1024 },
);
if (r.error) {
  console.error("docker failed:", r.error.message);
  process.exit(1);
}

// ---------- Parse: R passes iff EVERY test passes; W fails iff ≥1 test fails ----------
const byKey = new Map(); // `${variant}|${id}` -> { pass, fail }
for (const line of (r.stdout || "").split("\n")) {
  const m = line.match(/^RESULT (\w+) (\S+) (\S+) (?:status=(\d+)|BUILD_FAIL)/);
  if (!m) continue;
  const [, variant, id, , status] = m;
  const key = `${variant}|${id}`;
  if (!byKey.has(key)) byKey.set(key, { pass: 0, fail: 0 });
  const agg = byKey.get(key);
  if (status === "0") agg.pass++;
  else agg.fail++;
}

let pass = 0;
const failures = [];
const rows = [];
for (const job of jobs) {
  const sol = byKey.get(`sol|${job.id}`);
  const wrong = byKey.get(`wrong|${job.id}`);
  const total = job.tests.length;
  const rOk = sol && sol.fail === 0 && sol.pass + sol.fail === total;
  const wOk = wrong && wrong.fail > 0;
  const ok = rOk && wOk;
  if (ok) pass++;
  else {
    if (!rOk)
      failures.push(
        `${job.id} [R] REFERENCE MUST PASS but ${sol ? `${sol.fail}/${total} tests failed` : "no results"}`,
      );
    if (!wOk) failures.push(`${job.id} [W] WRONG SOLUTION MUST FAIL but all ${total} tests passed`);
  }
  rows.push(
    `${ok ? "OK " : "FAIL"} ${job.id} (R ${sol ? sol.fail : "?"}/${total} fail, W ${wrong ? wrong.fail : "?"}/${total} fail)`,
  );
}

rmSync(stage, { recursive: true, force: true });
for (const row of rows) console.log(row);
console.log(`\nverified: ${pass}/${rows.length} challenges two-sided OK`);
if (failures.length) {
  console.log(`\n${failures.length} FAILURES:`);
  for (const f of failures) console.log("  - " + f);
  process.exit(1);
}
