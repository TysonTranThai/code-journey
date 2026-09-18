/**
 * Two-sided compile+run smoke for c-beginner.
 *
 * Two-phase design (host clang ≠ sandbox gcc, and in-container Node cannot
 * resolve the runtime's extensionless imports):
 *   Phase 1 (host, tsx): import the REAL c-runtime.ts + cb-solutions.mjs,
 *     stage solution.c + byte-identical test files for every challenge into
 *     a staging dir, plus a plain-JS runner script.
 *   Phase 2 (container): the runner compiles+runs each test with the real
 *     sandbox gcc and writes a results JSON.
 *
 * Usage (repo root):
 *   node --import tsx --import ./scripts/worker-imports.mjs scripts/content-authoring/_cb_smoke.mjs [id-filter]
 */
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const mod = await import("../../src/workers/c-runtime.ts");
const rt = mod.default ?? mod;
const { buildCTestFile, cSanitizeName, C_STANDARD_FLAG, C_TEST_WARNING_FLAGS } = rt;

const REPO = process.cwd();
const COURSE = path.join(REPO, "src/content/tracks/c/courses/c-beginner");
const { R, W } = await import("./cb-solutions.mjs");

const only = process.argv[2] ?? "";

const challenges = new Map();
function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith(".json") && !e.name.endsWith(".vi.json")) {
      const d = JSON.parse(readFileSync(p, "utf8"));
      if (d && d.id && Array.isArray(d.tests)) challenges.set(d.id, { d, p });
    }
  }
}
walk(COURSE);

const selected = [...challenges.entries()].filter(([id]) => !only || id.includes(only));
console.log("challenges:", selected.length, only ? `(filter: ${only})` : "");
if (selected.length === 0) process.exit(2);

// ---- Phase 1: stage everything -------------------------------------------
const stage = path.join(tmpdir(), "cb-smoke");
rmSync(stage, { recursive: true, force: true });
mkdirSync(stage, { recursive: true });

const jobs = [];
for (const [id, { d }] of selected) {
  const job = { id, tests: [] };
  const solSrc = R[id] ?? null;
  const wrongSrc = W[id] ?? null;
  if (!solSrc) {
    console.log("MISSING R:", id);
    continue;
  }
  if (!wrongSrc) {
    console.log("MISSING W:", id);
    continue;
  }
  writeFileSync(path.join(stage, `sol-${id}.c`), solSrc);
  writeFileSync(path.join(stage, `wrong-${id}.c`), wrongSrc);
  for (const t of d.tests) {
    const name = cSanitizeName(t.name);
    writeFileSync(path.join(stage, `test-${id}-${name}.c`), buildCTestFile(t));
    job.tests.push(name);
  }
  jobs.push(job);
}

// Runner: plain POSIX sh + node-free (loop in sh would be awkward; generate a
// tiny runner JSON instead and drive it from sh lines directly).
const lines = ["set -u", "cd /work"];
const checks = [];
for (const job of jobs) {
  for (const variant of ["sol", "wrong"]) {
    lines.push(`cp "sol-${job.id}.c" solution.c`); // placeholder, replaced below
    checks.push({ id: job.id, variant });
  }
}
// Simpler: emit explicit per-variant blocks.
lines.length = 2;
for (const job of jobs) {
  for (const [variant, file] of [
    ["sol", `sol-${job.id}.c`],
    ["wrong", `wrong-${job.id}.c`],
  ]) {
    lines.push(`cp "${file}" solution.c`);
    for (const name of job.tests) {
      const bin = `b-${variant}-${job.id}-${name}`;
      lines.push(
        `gcc ${C_STANDARD_FLAG} ${C_TEST_WARNING_FLAGS.split(" ").join(" ")} -o "/tmp/${bin}" "test-${job.id}-${name}.c" -lm 2> "err-${bin}.log"`,
      );
      lines.push(`if [ $? -ne 0 ]; then echo "RESULT ${variant} ${job.id} ${name} BUILD_FAIL"; continue; fi`);
      lines.push(`"/tmp/${bin}" > "out-${bin}.log" 2> "hint-${bin}.log"`);
      lines.push(`echo "RESULT ${variant} ${job.id} ${name} status=$?"`);
    }
  }
}
writeFileSync(path.join(stage, "run.sh"), lines.join("\n") + "\n");

// ---- Phase 2: one container pass ------------------------------------------
const r = spawnSync(
  "docker",
  ["run", "--rm", "--network", "none", "-v", `${stage}:/work`, "-w", "/work", "codejourney-sandbox:latest", "sh", "run.sh"],
  { encoding: "utf8", timeout: 600_000, maxBuffer: 64 * 1024 * 1024 },
);
if (r.error) {
  console.error("docker failed:", r.error.message);
  process.exit(1);
}

// ---- Parse ----------------------------------------------------------------
// Aggregate PER CHALLENGE: a reference "passes" when every test passes; a
// wrong "fails" (correctly) when AT LEAST ONE test fails.
const byKey = new Map(); // `${variant}|${id}` -> { pass, fail, building }
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
let rp = 0,
  rf = 0,
  wp = 0,
  wf = 0;
const refFails = [];
const wrongPasses = [];
for (const job of jobs) {
  const sol = byKey.get(`sol|${job.id}`);
  const wrong = byKey.get(`wrong|${job.id}`);
  if (!sol) continue;
  if (sol.fail === 0) rp++;
  else {
    rf++;
    refFails.push(job.id);
  }
  if (!wrong) continue;
  if (wrong.fail > 0) wf++;
  else {
    wp++;
    wrongPasses.push(job.id);
  }
}
console.log(`R: ${rp} pass / ${rf} fail   W: ${wf} fail / ${wp} wrongly-pass`);
if (process.env.CB_KEEP) console.log("stage kept at:", stage);
if (refFails.length) console.log("REF FAIL challenges:", [...new Set(refFails)].join(", "));
if (wrongPasses.length) console.log("WRONGLY PASSING challenges:", [...new Set(wrongPasses)].join(", "));
process.exit(rf + wp === 0 ? 0 : 1);
