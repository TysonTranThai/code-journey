/**
 * Java runtime smoke test: builds the real job script (java-runtime.ts) and
 * runs it inside the actual sandbox container via the same docker invocation
 * shape the worker uses. Verdicts mirror execute.ts parsing.
 * Run: npx tsx scripts/content-authoring/_smoke-java.mts
 */
import { spawnSync } from "node:child_process";
import { buildJavaJobScript } from "../../src/workers/java-runtime";

const SOLUTION_OK = String.raw`public class Solution {
    public static int add(int a, int b) { return a + b; }

    public static String shout(String s) {
        return s.toUpperCase() + "!";
    }

    public static void program() {
        System.out.println("hello from java");
    }
}`;

const SOLUTION_BAD = String.raw`public class Solution {
    public static int add(int a, int b) { return a - b; }
}`;

const TESTS = [
  {
    name: "add-works",
    code: String.raw`CjTestBase.checkEq(Solution.add(2, 3), 5, "add(2,3)");
CjTestBase.checkEq(Solution.shout("hey"), "HEY!", "shout");`,
  },
  {
    name: "program-output",
    code: String.raw`String out = CjTestBase.capture(() -> Solution.program());
CjTestBase.checkContains(out, "hello from java");`,
  },
  {
    name: "should-fail-on-bad-solution",
    code: String.raw`CjTestBase.checkEq(Solution.add(2, 3), 5, "add(2,3)");`,
  },
];

function runContainer(script: string): { stdout: string; stderr: string; exit: number } {
  const args = [
    "run",
    "--rm",
    "--network", "none",
    "--read-only",
    "--tmpfs", "/tmp:size=64m,exec,nosuid,nodev",
    "--tmpfs", "/job:size=16m,noexec,nosuid,nodev,uid=100,gid=101",
    "--memory", "512mb",
    "--memory-swap", "512mb",
    "--cpus", "0.5",
    "--pids-limit", "64",
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges",
    "--user", "sandbox",
    "-i",
    "codejourney-sandbox:latest",
    "sh",
  ];
  const r = spawnSync("docker", args, { input: script, encoding: "utf8", timeout: 90_000 });
  return { stdout: r.stdout ?? "", stderr: r.stderr ?? "", exit: r.status ?? -1 };
}

// 1. Reference solution: all markers status=0.
const ok = runContainer(buildJavaJobScript({ code: SOLUTION_OK, testFiles: TESTS }, "CJ_SMOKE_J"));
const okMarkers = ok.stdout.split("\n").filter((l) => l.startsWith("__TEST_RESULT__"));
console.log("REF markers:", okMarkers);
if (okMarkers.length !== 3 || !okMarkers.every((l) => l.endsWith("status=0"))) {
  console.error("REF FAILED. stderr:", ok.stderr.slice(0, 2000));
  process.exit(1);
}

// 2. Wrong solution: marker status=1 with an educational message.
const bad = runContainer(buildJavaJobScript({ code: SOLUTION_BAD, testFiles: TESTS }, "CJ_SMOKE_J"));
const badMarker = bad.stdout.split("\n").find((l) => l.includes("should-fail-on-bad-solution"));
console.log("WRONG marker:", badMarker, "| stderr hint:", bad.stderr.split("\n").find((l) => l.includes("expected"))?.slice(0, 120));
if (!badMarker || !badMarker.endsWith("status=1")) {
  console.error("WRONG-SOLUTION DID NOT FAIL. stderr:", bad.stderr.slice(0, 2000));
  process.exit(1);
}

// 3. Non-compiling solution: no markers at all (verdict "error" upstream).
const broken = runContainer(
  buildJavaJobScript({ code: "public class Solution { broken", testFiles: TESTS }, "CJ_SMOKE_J"),
);
const brokenMarkers = broken.stdout.split("\n").filter((l) => l.startsWith("__TEST_RESULT__"));
console.log("BROKEN markers (expect none):", brokenMarkers.length, "| has compiler msg:", broken.stderr.includes("did not compile"));
if (brokenMarkers.length !== 0) {
  console.error("BROKEN SOLUTION PRODUCED MARKERS");
  process.exit(1);
}

console.log("SMOKE OK — all three contracts verified in the real container");
