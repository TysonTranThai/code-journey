/**
 * Two-sided compile+run QA for c-intermediate.
 *
 * Two-phase design (host clang ≠ sandbox gcc, and in-container Node cannot
 * resolve the runtime's extensionless imports — same as _cb_smoke.mjs):
 *   Phase 1 (host, tsx): import the REAL c-runtime.ts + cint-solutions.mjs,
 *     stage solution.c + byte-identical test files for every challenge into
 *     a staging dir, plus a plain-POSIX-sh runner script.
 *   Phase 2 (container): the runner compiles+runs each test with the real
 *     sandbox gcc and prints RESULT lines; this script parses them.
 *
 * Usage (repo root):
 *   node --import tsx --import ./scripts/worker-imports.mjs \
 *     scripts/content-authoring/verify-challenges-cint.mjs [id-filter]
 *
 * Exit 0 iff every reference solution passes every test AND every wrong
 * solution fails at least one test.
 */
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const mod = await import("../../src/workers/c-runtime.ts");
const rt = mod.default ?? mod;
const { buildCTestFile, cSanitizeName, C_STANDARD_FLAG, C_TEST_WARNING_FLAGS } = rt;

const REPO = process.cwd();
const COURSE = path.join(REPO, "src/content/tracks/c/courses/c-intermediate");
const { R, W } = await import("./cint-solutions.mjs");

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
const stage = path.join(tmpdir(), "cint-verify");
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
  // Production parity: the runner writes the learner's submitted code —
  // which always begins with the challenge boilerplate — as solution.c.
  // Mirror that here so types/includes provided by the boilerplate exist.
  const pre = typeof d.boilerplate === "string" ? d.boilerplate : "";
  writeFileSync(path.join(stage, `sol-${id}.c`), pre + solSrc);
  writeFileSync(path.join(stage, `wrong-${id}.c`), pre + wrongSrc);
  for (const t of d.tests) {
    const name = cSanitizeName(t.name);
    writeFileSync(path.join(stage, `test-${id}-${name}.c`), buildCTestFile(t));
    job.tests.push(name);
  }
  jobs.push(job);
}

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
      lines.push(`timeout 20 "/tmp/${bin}" > "out-${bin}.log" 2> "hint-${bin}.log"`);
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

// ---- Parse (challenge-level: R must pass ALL its tests; W must fail AT
// LEAST ONE — a W passing some tests is expected and fine) ------------------
const rFail = new Map(); // id -> any test failed
const wFail = new Map(); // id -> any test failed
let rp = 0,
  rf = 0,
  wp = 0,
  wf = 0;
for (const line of (r.stdout || "").split("\n")) {
  const m = line.match(/^RESULT (\w+) (\S+) (\S+) (?:status=(\d+)|BUILD_FAIL)/);
  if (!m) continue;
  const [, variant, id, , status] = m;
  const failed = status !== "0";
  if (variant === "sol") {
    rp++;
    if (failed) {
      rf++;
      rFail.set(id, true);
    }
  } else {
    if (failed) {
      wf++;
      wFail.set(id, true);
    } else wp++;
  }
}
const refFails = [...rFail.keys()];
const wrongPasses = [...wFail.keys() // challenges whose W passed EVERY test
  .filter((id) => selected.some(([sid]) => sid === id))
  .filter((id) => !wFail.has(id))];
console.log(`R tests: ${rp - rf} pass / ${rf} fail   W tests: ${wf} fail / ${wp} pass`);
console.log(`challenge verdicts: ${selected.length - refFails.length - wrongPasses.length} clean, ${refFails.length} ref-fail, ${wrongPasses.length} wrongly-pass`);
if (refFails.length) console.log("REF FAIL challenges:", refFails.join(", "));
if (wrongPasses.length) console.log("WRONGLY PASSING challenges (W passed every test):", wrongPasses.join(", "));
process.exit(refFails.length + wrongPasses.length === 0 ? 0 : 1);
