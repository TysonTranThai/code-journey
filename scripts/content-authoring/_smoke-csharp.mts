/**
 * C# runtime smoke test: builds the real job script (csharp-runtime.ts) and
 * runs it inside the actual sandbox container via the same docker invocation
 * shape the worker uses. Verdicts mirror execute.ts parsing.
 * Run: npx tsx scripts/content-authoring/_smoke-csharp.mts
 */
import { spawnSync } from "node:child_process";
import { buildCSharpJobScript } from "../../src/workers/csharp-runtime";

const SOLUTION_OK = String.raw`using System;

public class Solution
{
    public static int Add(int a, int b) { return a + b; }

    public static string Shout(string s) { return s.ToUpper() + "!"; }

    public static void Program()
    {
        Console.WriteLine("hello from csharp");
    }
}`;

const SOLUTION_BAD = String.raw`using System;

public class Solution
{
    public static int Add(int a, int b) { return a - b; }
}`;

const SOLUTION_SYNTAX_ERROR = String.raw`using System;

public class Solution
{
    public static int Add(int a, int b) { return a + b }
}`;

const TESTS = [
  {
    name: "add-works",
    code: String.raw`Cj.Eq(Solution.Add(2, 3), 5, "Add(2,3)");
Cj.Eq(Solution.Shout("hey"), "HEY!", "Shout");`,
  },
  {
    name: "program-output",
    code: String.raw`string outText = Cj.Capture(() => Solution.Program());
Cj.Contains(outText, "hello from csharp", "output");`,
  },
  {
    name: "should-fail-on-bad-solution",
    code: String.raw`Cj.Eq(Solution.Add(2, 3), 5, "Add(2,3)");`,
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
    "--memory", "512m",
    "--memory-swap", "512m",
    "--cpus", "0.5",
    "--pids-limit", "64",
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges",
    "--user", "sandbox",
    "-i",
    "--entrypoint", "sh",
    "codejourney-sandbox:latest",
  ];
  const r = spawnSync("docker", args, { input: script, encoding: "utf8", timeout: 120_000, maxBuffer: 16 * 1024 * 1024 });
  if (r.error) throw r.error;
  return { stdout: r.stdout ?? "", stderr: r.stderr ?? "", exit: r.status ?? -1 };
}

function parse(stdout: string): Map<string, number> {
  const m = new Map<string, number>();
  for (const line of stdout.split("\n")) {
    const hit = line.match(/^__TEST_RESULT__ (.+?) status=(\d+)\s*$/);
    if (hit && hit[1] && hit[2]) m.set(hit[1], Number(hit[2]));
  }
  return m;
}

let failures = 0;

// 1. Good solution: all three tests pass.
const ok = runContainer(buildCSharpJobScript({ code: SOLUTION_OK, testFiles: TESTS }, "CJ_EOF_smoke1"));
const okResults = parse(ok.stdout);
console.log("good solution markers:", [...okResults.entries()]);
for (const t of TESTS) {
  if (okResults.get(t.name) !== 0) {
    console.error(`FAIL expected pass for ${t.name}`, ok.stderr.slice(-800));
    failures++;
  }
}

// 2. Bad solution: the two graded tests fail with an educational message.
const bad = runContainer(buildCSharpJobScript({ code: SOLUTION_BAD, testFiles: TESTS }, "CJ_EOF_smoke2"));
const badResults = parse(bad.stdout);
console.log("bad solution markers:", [...badResults.entries()]);
if (badResults.get("add-works") === 0 || badResults.get("should-fail-on-bad-solution") === 0) {
  console.error("FAIL wrong solution passed a graded test");
  failures++;
}
if (!bad.stderr.includes("expected 5, got -1") && !bad.stderr.includes("expected")) {
  console.error("FAIL missing educational failure hint; stderr tail:", bad.stderr.slice(-400));
  failures++;
}

// 3. Syntax error: NO markers, verdict "error" path (exit != 0, compiler output on stderr).
const syn = runContainer(buildCSharpJobScript({ code: SOLUTION_SYNTAX_ERROR, testFiles: TESTS }, "CJ_EOF_smoke3"));
const synResults = parse(syn.stdout);
console.log("syntax-error markers:", synResults.size, "exit:", syn.exit);
if (synResults.size !== 0) {
  console.error("FAIL syntax-error solution produced test markers (gate did not fire)");
  failures++;
}
if (syn.exit === 0 || !syn.stderr.includes("did not compile")) {
  console.error("FAIL syntax gate did not produce an educational compile error; stderr tail:", syn.stderr.slice(-400));
  failures++;
}

if (failures > 0) {
  console.error(`SMOKE FAILED: ${failures} problem(s)`);
  process.exit(1);
}
console.log("SMOKE OK: good solution passes all tests, wrong solution fails with hints, syntax gate fires");
