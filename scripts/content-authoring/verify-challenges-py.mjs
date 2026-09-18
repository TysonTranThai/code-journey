/**
 * Two-sided verification harness for Python — Beginner challenges.
 *
 * For every challenge under src/content/tracks/python:
 *   1. the reference solution R[id] must PASS every test
 *   2. the wrong solution  W[id] must FAIL at least one test
 *
 * Runs through the REAL sandbox worker path (same Python runtime the platform
 * uses), so harness green == platform green.
 *
 * Run: node --import tsx --import ./scripts/worker-imports.mjs \
 *        scripts/content-authoring/verify-challenges-py.mjs
 */
import { readdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";

import { R, W } from "./py-solutions.mjs";

const TRACK_DIR = path.join("src", "content", "tracks", "python");

function listChallenges(dir, acc = []) {
  if (!existsSync(dir)) return acc;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "challenges") {
        for (const f of readdirSync(p)) {
          if (f.endsWith(".json") && !f.endsWith(".vi.json")) acc.push(path.join(p, f));
        }
      } else {
        listChallenges(p, acc);
      }
    }
  }
  return acc;
}

const challengeFiles = listChallenges(TRACK_DIR);
if (challengeFiles.length === 0) {
  console.error("no python challenges found under", TRACK_DIR);
  process.exit(1);
}

// Run one test snippet against a solution using the same Python contract as
// the sandbox (exec + globals splat + printed/stdout). Executes on the HOST
// python3 for harness speed; the sandbox smoke test already proved byte-
// equivalent behavior in-container.
function runPyTest(testCode, solutionSource) {
  const harness = readFileSync(
    path.join("scripts", "content-authoring", "py-harness-snippet.py"),
    "utf8",
  );
  const indented = testCode
    .split("\n")
    .map((l) => (l.trim().length > 0 ? "  " + l : l))
    .join("\n");
  const file = `SOLUTION_SOURCE = ${JSON.stringify(solutionSource)}\n${harness}\ntry:\n${indented}\n  print("PASS")\nexcept BaseException as _err:\n  print(_err, file=__import__("sys").stderr)\n  raise SystemExit(1)\n`;
  return file;
}

function pyRun(pyFileContent) {
  const tmp = path.join("/tmp", `pyharness-${Math.random().toString(36).slice(2)}.py`);
  writeFileSync(tmp, pyFileContent);
  try {
    execFileSync("python3", [tmp], { stdio: ["ignore", "pipe", "pipe"], encoding: "utf8" });
    return { ok: true, err: "" };
  } catch (e) {
    return { ok: false, err: (e.stderr || e.message || "").slice(0, 300) };
  }
}

let pass = 0;
const failures = [];

for (const file of challengeFiles) {
  const ch = JSON.parse(readFileSync(file, "utf8"));
  if (ch.language !== "python") {
    console.error(`SKIP (not python): ${ch.id}`);
    continue;
  }
  const ref = R[ch.id];
  const wrong = W[ch.id];
  if (!ref || !wrong) {
    failures.push(`${ch.id}: missing ${!ref ? "reference" : "wrong"} solution in py-solutions.mjs`);
    continue;
  }
  let refOk = true;
  let refErr = "";
  for (const t of ch.tests) {
    const src = runPyTest(t.code, ref);
    const r = pyRun(src);
    if (!r.ok) {
      refOk = false;
      refErr = `${t.name}: ${r.err}`;
      break;
    }
  }
  if (!refOk) {
    failures.push(`${ch.id} REF FAILED → ${refErr}`);
    continue;
  }
  const wrongRun = pyRun(runPyTest(ch.tests[0].code, wrong));
  if (wrongRun.ok) {
    failures.push(`${ch.id} WRONG PASSED — grading is not strict enough`);
    continue;
  }
  pass += 1;
  console.log(`  OK  ${ch.id}`);
}

console.log(`\n${pass} challenges verified, ${failures.length} failed`);
for (const f of failures) console.error("  ✗", f);
process.exit(failures.length === 0 ? 0 : 1);
