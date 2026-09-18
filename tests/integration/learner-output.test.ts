import { describe, expect, it } from "vitest";

import { executeJob } from "@/workers/execute";

import { execFile } from "node:child_process";

/** Runs only when Docker is up — same convention as sandbox-isolation. */
const dockerUp = await new Promise<boolean>((resolve) => {
  execFile("docker", ["info", "--format", "{{.ServerVersion}}"], (err) => resolve(!err));
});

/**
 * Learner-facing output hygiene (learner request 2026-09-06): the grader's
 * runner marker lines (`__TEST_RESULT__ <name> status=N`) must never leak
 * into the verdict panel's "Console output" — they looked like errors and
 * leaked the grading protocol. The learner's solution.js is data server-side
 * (never executed), so a normal run's output is empty; crash output (error
 * verdict) still surfaces.
 */
describe.skipIf(!dockerUp)("executeJob strips grader protocol lines from learner output", () => {
  it("passing run: clean output, correct per-test parsing", async () => {
    const result = await executeJob({
      code: "<h1>Hi</h1>",
      testFiles: [
        {
          name: "has-an-h1",
          code: `if (!/<h1\\s*>/i.test(code)) throw new Error("No <h1> found");`,
        },
      ],
      timeoutMs: 15_000,
      memoryMb: 256,
    });

    expect(result.verdict).toBe("passed");
    expect(result.perTestResults.map((r) => r.name)).toEqual(["has-an-h1"]);
    expect(result.output).not.toContain("__TEST_RESULT__");
  });

  it("failing run: marker stripped, educational message still attached", async () => {
    const result = await executeJob({
      code: "<p>Hi</p>",
      testFiles: [
        {
          name: "requires-h1",
          code: `if (!/<h1\\s*>/i.test(code)) throw new Error("Replace <p> with <h1>.");`,
        },
      ],
      timeoutMs: 15_000,
      memoryMb: 256,
    });

    expect(result.verdict).toBe("failed");
    expect(result.output).not.toContain("__TEST_RESULT__");
    expect(result.perTestResults[0]?.passed).toBe(false);
    expect(result.perTestResults[0]?.message).toContain("Replace <p> with <h1>");
  });

  it("Java run captures learner stdout in output", async () => {
    const result = await executeJob({
      language: "java",
      code: `public class Solution {
    public static void main(String[] args) {
        System.out.println("Hi");
    }
}`,
      testFiles: [
        {
          name: "three-lines",
          code: `
String out = CjTestBase.capture(() -> Solution.main(new String[0]));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("Hello, Code Journey!", "My name is Java", "I am learning fast"), "exact three lines");
`,
        },
      ],
      timeoutMs: 15_000,
      memoryMb: 512,
    });

    expect(result.verdict).toBe("failed");
    expect(result.output).toContain("Hi");
    expect(result.perTestResults[0]?.passed).toBe(false);
    expect(result.perTestResults[0]?.message).toContain("exact three lines");
  });
});
