/**
 * Two-sided compile+run QA for csharp-beginner.
 *
 * Two-phase design (host has no dotnet, and in-container Node cannot resolve
 * the runtime's extensionless imports — same as verify-challenges-cint.mjs):
 *   Phase 1 (host, tsx): import the REAL csharp-runtime.ts + the solutions
 *     ledger, stage Solution.cs + byte-identical test files for every
 *     challenge into a staging dir, plus a plain-POSIX-sh runner script.
 *   Phase 2 (container): the runner compiles+runs each test with the real
 *     sandbox Roslyn and prints RESULT lines; this script parses them.
 *
 * Usage (repo root):
 *   node --import tsx --import ./scripts/worker-imports.mjs \
 *     scripts/content-authoring/verify-challenges-csharp.mjs [id-filter]
 *
 * Exit 0 iff every reference solution passes every test AND every wrong
 * solution fails at least one test.
 */
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const mod = await import("../../src/workers/csharp-runtime.ts");
const rt = mod.default ?? mod;
const { buildCSharpTestFile, csSanitizeName, CS_REF_GLOB } = rt;

const REPO = process.cwd();
const COURSE = path.join(REPO, "src/content/tracks/csharp/courses/csharp-beginner");
const SOLUTIONS = process.argv[3] ?? "./csharp-beginner-solutions.mjs";
const { R, W } = await import(SOLUTIONS);

const only = process.argv[2] ?? "";

const challenges = new Map();
function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith(".json") && !e.name.endsWith(".vi.json")) {
      const d = JSON.parse(readFileSync(p, "utf8"));
      if (d && d.id && Array.isArray(d.tests) && d.language === "csharp") challenges.set(d.id, { d, p });
    }
  }
}
walk(COURSE);

const selected = [...challenges.entries()].filter(([id]) => !only || id.includes(only));
console.log("challenges:", selected.length, only ? `(filter: ${only})` : "");
if (selected.length === 0) process.exit(2);

// ---- Phase 1: stage everything -------------------------------------------
const stage = path.join(tmpdir(), "csharp-verify");
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
  // which always begins with the challenge boilerplate — as Solution.cs.
  const pre = typeof d.boilerplate === "string" ? d.boilerplate : "";
  writeFileSync(path.join(stage, `sol-${id}.cs`), pre + solSrc);
  writeFileSync(path.join(stage, `wrong-${id}.cs`), pre + wrongSrc);
  for (const t of d.tests) {
    const name = csSanitizeName(t.name);
    writeFileSync(path.join(stage, `test-${id}-${name}.cs`), buildCSharpTestFile(t));
    job.tests.push(name);
  }
  jobs.push(job);
}

const lines = [
  "set -u",
  "cd /work",
  "export DOTNET_ROOT=/usr/share/dotnet DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1 DOTNET_CLI_HOME=/tmp HOME=/tmp",
  `CSC="dotnet /usr/share/dotnet/sdk/*/Roslyn/bincore/csc.dll"`,
  `REFS=""; for f in ${CS_REF_GLOB}; do REFS="$REFS -r:$f"; done`,
  `echo '{"runtimeOptions":{"tfm":"net10.0","rollForward":"LatestMinor","framework":{"name":"Microsoft.NETCore.App","version":"10.0.0"}}}' > rc.json`,
];
for (const job of jobs) {
  for (const [variant, file] of [
    ["sol", `sol-${job.id}.cs`],
    ["wrong", `wrong-${job.id}.cs`],
  ]) {
    lines.push(`cp "${file}" Solution.cs`);
    for (const name of job.tests) {
      const dll = `b-${variant}-${job.id}-${name}`;
      lines.push(`cp rc.json "/tmp/${dll}.runtimeconfig.json"`);
      lines.push(
        `$CSC -nologo -out:"/tmp/${dll}.dll" $REFS -main:CjTest Solution.cs "test-${job.id}-${name}.cs" > "err-${dll}.log" 2>&1`,
      );
      lines.push(`if [ $? -ne 0 ]; then echo "RESULT ${variant} ${job.id} ${name} BUILD_FAIL"; continue; fi`);
      lines.push(`timeout 20 dotnet "/tmp/${dll}.dll" > "out-${dll}.log" 2> "hint-${dll}.log"`);
      lines.push(`echo "RESULT ${variant} ${job.id} ${name} status=$?"`);
    }
  }
}
writeFileSync(path.join(stage, "run.sh"), lines.join("\n") + "\n");

// ---- Phase 2: one container pass ------------------------------------------
const r = spawnSync(
  "docker",
  ["run", "--rm", "--network", "none", "-v", `${stage}:/work`, "-w", "/work", "codejourney-sandbox:latest", "sh", "run.sh"],
  { encoding: "utf8", timeout: 900_000, maxBuffer: 64 * 1024 * 1024 },
);
if (r.error) {
  console.error("docker failed:", r.error.message);
  process.exit(1);
}

// ---- Parse (challenge-level: R must pass ALL its tests; W must fail AT
// LEAST ONE — a W passing some tests is expected and fine) ------------------
const rFail = new Map(); // id -> any test failed
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
    } else wp++;
  }
}
const wrongAllPass = [];
const perIdWFail = new Map();
for (const line of (r.stdout || "").split("\n")) {
  const m = line.match(/^RESULT wrong (\S+) (\S+) (?:status=(\d+)|BUILD_FAIL)/);
  if (!m) continue;
  const [, id, , status] = m;
  if (status === "0") perIdWFail.set(id, (perIdWFail.get(id) ?? 0));
  else perIdWFail.set(id, (perIdWFail.get(id) ?? 0) + 1);
}
for (const [id] of selected) {
  if (!W[id]) continue;
  if (!(perIdWFail.get(id) > 0)) wrongAllPass.push(id);
}
const refFails = [...rFail.keys()];
console.log(`R tests: ${rp - rf} pass / ${rf} fail   W tests: ${wf} fail / ${wp} pass`);
console.log(
  `challenge verdicts: ${selected.length - refFails.length - wrongAllPass.length} clean, ${refFails.length} ref-fail, ${wrongAllPass.length} wrongly-pass`,
);
if (refFails.length) console.log("REF FAIL challenges:", refFails.join(", "));
if (wrongAllPass.length) console.log("WRONGLY PASSING challenges (W passed every test):", wrongAllPass.join(", "));
process.exit(refFails.length + wrongAllPass.length === 0 ? 0 : 1);
