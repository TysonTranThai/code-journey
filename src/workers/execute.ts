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
  language?: "javascript" | "python" | "cpp" | "java" | "c" | "csharp";
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
      output: truncateOutput(result.stderr || learnerOutput(result.stdout) || "no output produced"),
    };
  }

  const allPassed = perTestResults.every((r) => r.passed);
  return {
    verdict: allPassed ? "passed" : "failed",
    perTestResults,
    runtimeMs,
    output: truncateOutput(learnerOutput(result.stdout)),
  };
}

/**
 * Learner-facing console output: hide the grader's own protocol lines (the
 * per-test `__TEST_RESULT__ …` markers and the harness's `PASS`
 * confirmations) so the console shows only what the learner's code printed.
 * These lines are grading plumbing — displaying them leaked the marker
 * format to learners and looked like an error even on success.
 */
function learnerOutput(stdout: string): string {
  return stdout
    .split("\n")
    .filter((line) => {
      const trimmed = line.trim();
      return !trimmed.startsWith(TEST_RESULT_MARKER) && trimmed !== "PASS";
    })
    .join("\n");
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
  // CHAL-05 + learner bug report 2026-09-13: the failure hint must be the
  // human message a learner can act on. When a test snippet itself throws
  // outside the harness try (author bug) or the file fails to parse, Node
  // prints a full crash report: `file:///job/test-….mjs:5` location line, an
  // unprefixed echo of the offending source line, a caret marker, and `at …`
  // stack frames. None of that is a hint — a filesystem URL as the failure
  // reason is exactly what the learner complained about. Python/other
  // runtimes never emit those shapes, so the filters are safe globally.
  const stderrLines = result.stderr
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.length > 0 && !l.startsWith("node:"))
    .filter((l) => {
      if (l.startsWith("file://")) return false; // Node location line
      if (l.startsWith("at ")) return false; // stack frame
      if (/^[|^\s]*\^/.test(l)) return false; // caret marker
      // Crash-report tail line: `Node.js v22.17.0` at the very end.
      if (/^Node\.js v\d+/.test(l)) return false;
      // Unprefixed source-echo line: looks like JS source (call/keyword
      // start) rather than a sentence. Exception messages like
      // "ReferenceError: x is not defined" are kept.
      if (/^(const|let|var|await|async|function|return|if|for|while|import|export|class|throw|new\s|[a-zA-Z_$][\w$.]*\s*\()/.test(l)) return false;
      return true;
    });

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
