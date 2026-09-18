/**
 * Smoke test: Python execution through the real sandbox worker path.
 * Run: npx tsx scripts/content-authoring/py-sandbox-smoke.ts
 * Requires the codejourney-sandbox image (pnpm sandbox:build) and Docker.
 */
import { runSandboxed } from "@/workers/sandbox";

const passingSolution = `
def add(a, b):
    return a + b

total = add(2, 3)
print(f"total={total}")
`;

const brokenSolution = `
def add(a, b):
    return a - b
`;

async function main() {
  const tests = [
    {
      name: "adds numbers",
      code: `
assert add(2, 3) == 5, "add(2, 3) should be 5"
assert add(-1, 1) == 0, "add(-1, 1) should be 0"
`,
    },
    {
      name: "prints the total",
      code: `
assert printed == ["total=5"], f"expected printed ['total=5'], got {printed}"
`,
    },
  ];

  const pass = await runSandboxed({
    code: passingSolution,
    testFiles: tests,
    timeoutMs: 10_000,
    memoryMb: 256,
    language: "python",
  });
  console.log("== reference solution ==", JSON.stringify(pass));
  if (pass.exitCode !== 0) {
    console.error("REFERENCE FAILED", pass.stdout, pass.stderr);
    process.exit(1);
  }

  const fail = await runSandboxed({
    code: brokenSolution,
    testFiles: tests,
    timeoutMs: 10_000,
    memoryMb: 256,
    language: "python",
  });
  console.log("== wrong solution ==", JSON.stringify({ exitCode: fail.exitCode, stderr: fail.stderr.slice(0, 200) }));
  if (fail.exitCode === 0) {
    console.error("WRONG SOLUTION PASSED — grading is broken");
    process.exit(1);
  }

  const inputProbe = await runSandboxed({
    code: "x = input('give: ')\nprint(x)",
    testFiles: [{ name: "input blocked", code: "pass" }],
    timeoutMs: 10_000,
    memoryMb: 256,
    language: "python",
  });
  console.log("== input() probe ==", JSON.stringify({ exitCode: inputProbe.exitCode, stderr: inputProbe.stderr.slice(0, 120) }));
  if (inputProbe.exitCode === 0) {
    console.error("input() should be blocked in graded runs");
    process.exit(1);
  }

  console.log("PYTHON SANDBOX SMOKE: ALL GOOD");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
