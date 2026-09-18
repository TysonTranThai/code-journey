/**
 * One-off probe — Vietnamese test names through the REAL learner path
 * (executeJob = runSandboxed + marker parse + hint filtering), using the
 * runtime's actual test-file contract (snippets assert on the `code`
 * variable — the learner solution read from /job/solution.js).
 *
 * Verifies: (1) passing + failing test names keep diacritics readable,
 * (2) failure hints are the assertion errors learners can act on,
 * (3) Node crash-report lines (file:///job/... / Node.js vXX) never leak.
 *
 * Run: node --import tsx --import ./scripts/worker-imports.mjs \
 *        scripts/content-authoring/_verify_vi_names.mjs
 */
import { executeJob } from "../../src/workers/execute.ts";

// Learner solution text — test 1 (fail) checks a greeting it doesn't have,
// test 2 (pass) checks one it does, test 3 (crash shape) calls an
// undefined helper — the exact shape of the learner's file:/// report.
const SOLUTION = `const greeting = "xin chào";\nconsole.log(greeting);\n`;

const payload = await executeJob({
  language: "javascript",
  code: SOLUTION,
  timeoutMs: 30_000,
  memoryMb: 512,
  testFiles: [
    {
      name: "lỗi chờ chính xác", // <- failing test, name from the bug report
      code: `if (!code.includes("tạm biệt")) throw new Error("chưa chứa lời tạm biệt");\n`,
    },
    {
      name: "đầu ra đúng định dạng", // <- passing test
      code: `if (!code.includes("xin chào")) throw new Error("thiếu lời chào");\n`,
    },
    {
      name: "trợ giúp xác định", // <- crash shape: undefined helper (author bug)
      code: `undefined_helper(code);\n`,
    },
  ],
});

console.log("=== verdict payload ===");
console.log(JSON.stringify(payload, null, 2).slice(0, 3500));

const names = payload.perTestResults.map((t) => t.name);
const mush = names.filter((n) => /^l-i-|-ch-o-ch-|-x-c$/.test(n));
const leak =
  JSON.stringify(payload).includes("file://") ||
  JSON.stringify(payload).includes("node:internal") ||
  JSON.stringify(payload).includes("Node.js v");

const byName = new Map(payload.perTestResults.map((t) => [t.name, t]));
const passed = [...byName.values()].filter((t) => t.passed);
const failed = [...byName.values()].filter((t) => !t.passed);
const hintsReadable = failed.every((t) => t.message.length > 0 && !/^\s*$/.test(t.message));

console.log("=== checks ===");
console.log("names reported:", JSON.stringify(names));
console.log("diacritics preserved (no dash-mush):", mush.length === 0 ? "PASS" : `FAIL ${mush}`);
console.log("no file:///internal/Node.js-version leak:", leak ? "FAIL" : "PASS");
console.log("one test passed with VI name:", passed.some((t) => t.name === "đầu-ra-đúng-định-dạng") ? "PASS" : `FAIL ${JSON.stringify(passed.map((t) => t.name))}`);
console.log("all failure hints readable:", hintsReadable ? `PASS (${failed.map((t) => `"${t.message}"`).join(", ")})` : "FAIL");
if (mush.length > 0 || leak || passed.length !== 1) process.exit(1);
console.log("ALL CHECKS PASS");
