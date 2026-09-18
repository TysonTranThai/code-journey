/**
 * Two-sided verification harness — Python — Intermediate challenges.
 *
 * For every challenge under the python-intermediate course:
 *   1. the reference solution R[id] must PASS every test
 *   2. the wrong solution  W[id] must FAIL at least one test
 *
 * Same execution engine as verify-challenges-py.mjs (SOLUTION_SOURCE harness +
 * local python3), so harness green == grading-code green; the sandbox worker
 * uses the identical harness contract.
 *
 * Run: node scripts/content-authoring/verify-challenges-pi.mjs
 */
import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";

import { R, W } from "./pi-solutions.mjs";

const COURSE_DIR = path.join(
  "src",
  "content",
  "tracks",
  "python",
  "courses",
  "python-intermediate",
);

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

function runPyTest(testCode, solutionSource) {
  const harness = [
    "import json, math, os, re, sys, io, unittest, itertools, functools, collections, datetime, pathlib, tempfile, hashlib, sqlite3, asyncio",
    "",
    "def _no_input(*_a, **_k):",
    "    raise RuntimeError('input() is disabled in challenge grading')",
    "",
    "input = _no_input",
    "raw_input = _no_input",
    "",
  ].join("\n");
  const indented = testCode
    .split("\n")
    .map((l) => "  " + l)
    .join("\n");
  const file = `SOLUTION_SOURCE = ${JSON.stringify(solutionSource)}\n${harness}\ntry:\n${indented}\n  print("PASS")\nexcept BaseException as _err:\n  print(_err, file=__import__("sys").stderr)\n  raise SystemExit(1)\n`;
  return file;
}

function pyRun(pyFileContent) {
  const tmp = path.join("/tmp", `piharness-${Math.random().toString(36).slice(2)}.py`);
  writeFileSync(tmp, pyFileContent);
  try {
    execFileSync("python3", [tmp], { stdio: ["ignore", "pipe", "pipe"], encoding: "utf8" });
    return { ok: true, err: "" };
  } catch (e) {
    return { ok: false, err: (e.stderr || e.message || "").slice(0, 400) };
  }
}

let pass = 0;
const failures = [];
const challengeFiles = listChallenges(COURSE_DIR);

for (const file of challengeFiles) {
  const ch = JSON.parse(readFileSync(file, "utf8"));
  if (ch.language !== "python") {
    console.error(`SKIP (not python): ${ch.id}`);
    continue;
  }
  const ref = R[ch.id];
  const wrong = W[ch.id];
  if (!ref || !wrong) {
    failures.push(`${ch.id}: missing ${!ref ? "reference" : "wrong"} solution in pi-solutions.mjs`);
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
  // every test must fail on the wrong solution at some point; check all tests
  let wrongFailsAny = false;
  for (const t of ch.tests) {
    const wrongRun = pyRun(runPyTest(t.code, wrong));
    if (!wrongRun.ok) {
      wrongFailsAny = true;
      break;
    }
  }
  if (!wrongFailsAny) {
    failures.push(`${ch.id} WRONG PASSED — grading is not strict enough`);
    continue;
  }
  pass += 1;
}

console.log(`pi harness: ${pass}/${challengeFiles.length} two-sided verified`);
if (failures.length) {
  console.error(`FAILURES (${failures.length}):`);
  for (const f of failures) console.error(" -", f);
  process.exit(1);
}
