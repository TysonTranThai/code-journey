/**
 * One-off probe: compile+run the first test of a challenge against its R/W
 * solution using the REAL sandbox test-file builder. Usage:
 *   npx tsx scripts/content-authoring/_probe_m18.mjs <challengeId>
 */
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, writeFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildCppTestFile } from "../../src/workers/cpp-runtime.ts";

const COURSE = path.resolve("src/content/tracks/hsg/courses/hsg-advanced");
const SOLUTIONS = "./hsg-advanced-solutions.mjs";
const only = process.argv[2];
const { R, W } = await import(SOLUTIONS);

const found = {};
function walk(dir) {
  for (const f of readdirSync(dir)) {
    const p = path.join(dir, f);
    if (f.endsWith(".json") && !f.endsWith(".vi.json")) {
      try {
        const d = JSON.parse(readFileSync(p, "utf8"));
        if (d && d.id && Array.isArray(d.tests)) found[d.id] = d;
      } catch {}
    } else {
      try { walk(p); } catch {}
    }
  }
}
walk(COURSE);
const ch = found[only];
if (!ch) { console.error("challenge not found:", only, "| known:", Object.keys(found).filter(k => k.includes("m18")).join(", ")); process.exit(1); }

const dir = mkdtempSync(path.join(os.tmpdir(), "cjprobe-"));
for (const [tag, body] of [["R", R[only]], ["W", W[only]]]) {
  if (!body) { console.log(tag, ": missing body"); continue; }
  for (let i = 0; i < ch.tests.length; ++i) {
    const test = ch.tests[i];
    writeFileSync(path.join(dir, "solution.cpp"), body);
    writeFileSync(path.join(dir, "t.cpp"), buildCppTestFile(test));
    const c = spawnSync("g++", ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", path.join(dir, "t.cpp"), "-o", path.join(dir, "t")], { encoding: "utf8", timeout: 90000 });
    if (c.status !== 0) {
      console.log(tag, "test", i, "COMPILE-FAIL:", (c.stderr || "").slice(0, 400).split("\n").slice(-4).join(" | "));
      continue;
    }
    const r = spawnSync(path.join(dir, "t"), { encoding: "utf8", timeout: 30000 });
    const status = r.status === 0 && r.stdout.startsWith("PASS") ? "pass" : (r.status === 1 && r.stdout === "" ? "FAIL" : "rc" + r.status);
    console.log(tag, "test", i, status, r.stderr ? ("|" + r.stderr.slice(0, 160).replace(/\n/g, " ")) : "");
  }
}
rmSync(dir, { recursive: true, force: true });
