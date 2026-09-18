/**
 * Live E2E probe for the C runtime path: builds the job script exactly as
 * the worker would (importing src/workers/c-runtime.ts through the same
 * worker-imports preload used by verify harnesses) and executes it in the
 * real sandbox container. Verifies three paths:
 *   1. reference solution  -> all tests pass (status=0 markers, PASS)
 *   2. wrong solution      -> deterministic per-test failures with hints
 *   3. non-compiling code  -> verdict "error" shape (no markers, gcc output)
 * Run from repo root: node --import tsx --import ./scripts/worker-imports.mjs scripts/content-authoring/_c_runtime_e2e.mjs
 */
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const { buildCJobScript } = await import("../../src/workers/c-runtime.ts");

const tests = [
  {
    name: "adds-basic",
    code: `CHECK_EQ(add(2, 2), 4);
CHECK_EQ(add(-1, 1), 0);`,
  },
  {
    name: "adds-large",
    code: `CHECK_EQ(add(1'000, 337), 1'337);
CHECK_NEAR(addf(0.5, 0.25), 0.75, 1e-9);`,
  },
  {
    name: "greets-output",
    code: `const char* out = cj_capture(program);
CHECK_CONTAINS(out, "Hello, C!");
CHECK_STR_EQ(add_str("a", "b"), "ab");`,
  },
];

const solution = `#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int add(int a, int b) { return a + b; }

double addf(double a, double b) { return a + b; }

/* add_str concatenates two short strings into a caller-provided buffer. */
const char* add_str(const char* a, const char* b) {
    static char buf[128];
    snprintf(buf, sizeof buf, "%s%s", a, b);
    return buf;
}

void program(void) {
    printf("Hello, C!\\n");
    printf("second line\\n");
}

int main(void) { return 0; }
`;

const wrong = solution.replace("return a + b;", "return a - b;");

const broken = solution.replace("#include <stdio.h>\n", "");

function runJob(code, label) {
  const delim = "CJ_EOF_test" + Math.random().toString(16).slice(2);
  const script = buildCJobScript({ code, testFiles: tests }, delim);
  const dir = mkdtempSync(join(tmpdir(), "cje2e-"));
  writeFileSync(join(dir, "job.sh"), script);
  const r = spawnSync(
    "docker",
    ["run", "--rm", "--network", "none", "-i", "codejourney-sandbox:latest", "sh"],
    { input: script, encoding: "utf8", timeout: 90_000, maxBuffer: 8 * 1024 * 1024 },
  );
  rmSync(dir, { recursive: true, force: true });
  return { stdout: r.stdout ?? "", stderr: r.stderr ?? "", status: r.status, label };
}

function assert(cond, msg, detail) {
  if (!cond) {
    console.error(`E2E FAIL: ${msg}`);
    if (detail) {
      console.error("--- stdout ---");
      console.error(detail.stdout?.slice(0, 2000));
      console.error("--- stderr ---");
      console.error(detail.stderr?.slice(0, 2000));
    }
    process.exit(1);
  }
  console.log(`ok: ${msg}`);
}

// 1) reference passes everything
const good = runJob(solution, "reference");
for (const t of tests) {
  assert(good.stdout.includes(`__TEST_RESULT__ ${t.name} status=0`), `reference: ${t.name} passes`, good);
}
assert(good.stdout.includes("PASS"), "reference: harness PASS line present");

// 2) wrong solution fails the value tests but still compiles
const bad = runJob(wrong, "wrong");
assert(bad.stdout.includes("__TEST_RESULT__ adds-basic status=1"), "wrong: adds-basic fails");
assert(bad.stdout.includes("__TEST_RESULT__ adds-large status=1"), "wrong: adds-large fails");
assert(bad.stderr.includes("expected add(2, 2) == 4 but got 0 vs 4"), "wrong: educational hint present", bad);
assert(bad.stdout.includes("__TEST_RESULT__ greets-output status=0"), "wrong: untouched function still passes");

// 3) compile error -> no markers, gcc output on stderr
const err = runJob(broken, "broken");
assert(!err.stdout.includes("__TEST_RESULT__"), "broken: no markers emitted");
assert(err.stderr.includes("stdio.h"), "broken: gcc error surfaced");
assert(err.stderr.includes("did not compile"), "broken: educational compile-error prefix");

console.log("C runtime E2E: all three paths verified");
