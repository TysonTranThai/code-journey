/** Quick two-sided compile+run check for cpp-advanced (scripts dev loop). */
import { spawnSync } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildCppTestFile, cppSanitizeName } from "../../src/workers/cpp-runtime.ts";

const COURSE = path.resolve("src/content/tracks/cpp/courses/cpp-advanced");
const { R, W } = await import("./cppa-solutions.mjs");

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
console.log("challenges:", challenges.size);
let rp = 0, rf = 0, wp = 0, wf = 0;
for (const [id, { d }] of challenges) {
  const tmp = mkdtempSync(path.join(os.tmpdir(), "cppa-"));
  const runSol = (src) => {
    writeFileSync(path.join(tmp, "solution.cpp"), src);
    for (const t of d.tests) {
      const name = cppSanitizeName(t.name);
      writeFileSync(path.join(tmp, `test-${name}.cpp`), buildCppTestFile(t));
      const b = spawnSync("g++", ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-o", `/tmp/cppa-t-${name}`, `test-${name}.cpp`], { cwd: tmp, encoding: "utf8" });
      if (b.status !== 0) return { ok: false, why: `build: ${(b.stderr || "").split("\n").filter(Boolean).slice(0, 4).join(" | ")}` };
      const r = spawnSync(`/tmp/cppa-t-${name}`, { encoding: "utf8", timeout: 30000 });
      if (r.status !== 0) return { ok: false, why: (r.stderr || r.stdout || "no output").split("\n").filter(Boolean).slice(0, 2).join(" | ") };
    }
    return { ok: true };
  };
  if (!R[id]) { console.log("MISSING R:", id); rf++; }
  else if (!runSol(R[id]).ok) { console.log("REF FAIL:", id, "—", runSol(R[id]).why); rf++; }
  else rp++;
  if (!W[id]) { console.log("MISSING W:", id); wf++; }
  else if (runSol(W[id]).ok) { console.log("WRONG PASSES(!):", id); wp++; }
  else wf++;
}
console.log(`R: ${rp} pass / ${rf} fail   W: ${wf} fail / ${wp} wrongly-pass`);
