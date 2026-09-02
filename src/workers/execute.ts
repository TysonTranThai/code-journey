import "server-only";

import { truncateOutput, type PerTestResult, type VerdictPayload } from "@/lib/execution/types";
import { runSandboxed } from "./sandbox";

/**
 * Real job execution (replaces the 03-01 stub): runs the student code +
 * challenge tests inside the hardened sandbox and maps the container output
 * to the typed verdict model.
 *
 * Verdict mapping:
 *  - timeout       → "timeout" (with the educational infinite-loop message)
 *  - all tests OK  → "passed"
 *  - ≥1 test fail  → "failed" with per-test results
 *  - crash before tests (syntax error etc.) → "error" with the compiler output
 */

const TEST_RESULT_MARKER = "__TEST_RESULT__";

export async function executeJob(payload: {
  code: string;
  testFiles: { name: string; code: string }[];
  timeoutMs: number;
  memoryMb: number;
}): Promise<VerdictPayload> {
  const startedAt = Date.now();
  const result = await runSandboxed(payload);
  const runtimeMs = Date.now() - startedAt;

  if (result.timedOut) {
    return {
      verdict: "timeout",
      perTestResults: [],
      runtimeMs,
      output: truncateOutput(
        "Your code took too long to finish — check for infinite loops or operations that never complete.",
      ),
    };
  }

  // Parse per-test results from the marker lines.
  const perTestResults = parseTestResults(result);

  if (perTestResults.length === 0) {
    // Nothing ran — syntax error, missing file, or crash before tests.
    return {
      verdict: "error",
      perTestResults: [],
      runtimeMs,
      output: truncateOutput(result.stderr || result.stdout || "no output produced"),
    };
  }

  const allPassed = perTestResults.every((r) => r.passed);
  return {
    verdict: allPassed ? "passed" : "failed",
    perTestResults,
    runtimeMs,
    output: truncateOutput(result.stdout),
  };
}

function parseTestResults(result: { stdout: string; stderr: string }): PerTestResult[] {
  const perTest = new Map<string, { passed: boolean; message: string }>();
  // The runner script prints one authoritative marker line AFTER each test
  // run with its real exit status.
  for (const line of result.stdout.split("\n")) {
    const match = line.match(new RegExp(`${TEST_RESULT_MARKER} (.+?) status=(\\d+)\\s*$`));
    if (!match) continue;
    const [, rawName, status] = match;
    if (!rawName || !status) continue;
    perTest.set(rawName, {
      passed: status === "0",
      message: "",
    });
  }

  // Attach educational messages: on failure, the test's stderr line (the
  // thrown Error message) — CHAL-05: never a bare boolean.
  const stderrLines = result.stderr
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.length > 0 && !l.startsWith("node:"));

  const results: PerTestResult[] = [];
  for (const [name, outcome] of perTest) {
    if (outcome.passed) {
      results.push({ name, passed: true, message: "" });
    } else {
      const hint = stderrLines[0] ?? "Test failed — check your solution against the requirements.";
      results.push({ name, passed: false, message: hint });
      // One hint per failing test: consume lines as we go.
      stderrLines.shift();
    }
  }
  return results;
}
