import "server-only";

import { spawn } from "node:child_process";

/**
 * Hardened container execution (03-CONTEXT D-02).
 *
 * EVERY student-code run goes through `runSandboxed`. The container is
 * started with the full hardening set from the OWASP Docker Security
 * baseline:
 *   --network none        no egress whatsoever
 *   --read-only + tmpfs   ephemeral, write-only /tmp (16 MB)
 *   --memory / --cpus     resource ceilings
 *   --pids-limit          fork-bomb containment
 *   --cap-drop ALL        no kernel capabilities
 *   --security-opt no-new-privileges  no privilege escalation
 *   non-root user         uid/gid 100:101 (sandbox user in the image)
 *
 * Wall-clock timeout is enforced HERE (docker kill after `timeoutMs`) —
 * the container itself cannot be trusted to self-terminate.
 *
 * SECURITY STATUS: hardened per baseline; NOT claimed production-grade
 * until the malicious-sample isolation suite passes AND an external
 * security review happens (docs/SECURITY.md honesty rule).
 */

const SANDBOX_IMAGE = process.env.SANDBOX_IMAGE ?? "codejourney-sandbox:latest";
/** Hard ceiling on wall-clock time regardless of requested timeout. */
const MAX_TIMEOUT_MS = 30_000;
/** Output caps: a runaway process cannot flood memory/verdicts. */
const MAX_OUTPUT_BYTES = 256 * 1024;

export interface SandboxResult {
  timedOut: boolean;
  exitCode: number | null;
  stdout: string;
  stderr: string;
}

export function runSandboxed(options: {
  code: string;
  testFiles: { name: string; code: string }[];
  timeoutMs: number;
  memoryMb: number;
}): Promise<SandboxResult> {
  const timeoutMs = Math.min(Math.max(options.timeoutMs, 1000), MAX_TIMEOUT_MS);
  return new Promise((resolve, reject) => {
    // Materialize files into a docker-build-compatible context via stdin:
    // we create the job dir in-container through a shell script passed as
    // the command. Files are written to tmpfs (world-writable, ephemeral);
    // code and tests are passed as argv-safe heredoc content via stdin.
    const script = buildJobScript(options.code, options.testFiles);

    const args = [
      "run",
      "--rm", // ephemeral
      "--network",
      "none", // no egress
      "--read-only", // immutable rootfs
      "--tmpfs",
      "/tmp:size=16m,noexec,nosuid,nodev", // scratch space only
      "--tmpfs",
      "/job:size=16m,noexec,nosuid,nodev,uid=100,gid=101", // job files
      "--memory",
      `${options.memoryMb}m`,
      "--memory-swap",
      `${options.memoryMb}m`, // no swap — hard ceiling
      "--cpus",
      "0.5",
      "--pids-limit",
      "64", // fork-bomb containment
      "--cap-drop",
      "ALL",
      "--security-opt",
      "no-new-privileges",
      "--user",
      "sandbox", // non-root
      "-i", // stdin for the job script
      SANDBOX_IMAGE,
      "sh", // reads the script from stdin
    ];

    const child = spawn("docker", args, {
      stdio: ["pipe", "pipe", "pipe"],
      // Never let docker inherit env secrets.
      env: {
        PATH: process.env.PATH ?? "/usr/local/bin:/usr/bin:/bin",
        HOME: "/tmp",
        NODE_ENV: process.env.NODE_ENV,
      } as NodeJS.ProcessEnv,
    }) as import("node:child_process").ChildProcessWithoutNullStreams;

    let timedOut = false;
    let stdout = "";
    let stderr = "";
    let killedBySize = false;

    const timer = setTimeout(() => {
      timedOut = true;
      child.kill("SIGKILL");
    }, timeoutMs);

    child.stdout.on("data", (chunk: Buffer) => {
      if (stdout.length < MAX_OUTPUT_BYTES) stdout += chunk.toString("utf8");
      else killedBySize = true;
    });
    child.stderr.on("data", (chunk: Buffer) => {
      if (stderr.length < MAX_OUTPUT_BYTES) stderr += chunk.toString("utf8");
      else killedBySize = true;
    });

    child.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });

    child.on("close", (exitCode) => {
      clearTimeout(timer);
      if (killedBySize) {
        stderr += "\n… (output truncated)";
      }
      resolve({ timedOut, exitCode, stdout, stderr });
    });

    // Feed the job script, then close stdin so sh executes it.
    child.stdin.write(script);
    child.stdin.end();
  });
}

/**
 * POSIX sh script that writes the student code + test harness into /job
 * (tmpfs) and runs them with node. Heredocs with quoted delimiters mean
 * NO shell expansion — student code is data, never interpreted by sh.
 */
function buildJobScript(code: string, testFiles: { name: string; code: string }[]): string {
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("solution.js", code));
  for (const test of testFiles) {
    parts.push(heredoc(`test-${sanitizeName(test.name)}.mjs`, buildTestFile(test)));
  }
  // Run each test file; each exits 0 (pass) or non-zero (fail). Tests run
  // sequentially and all report (no early stop) — the marker line AFTER each
  // run is the authoritative per-test result the parser reads.
  for (const test of testFiles) {
    parts.push(
      `node "test-${sanitizeName(test.name)}.mjs" ; ` +
        `echo "__TEST_RESULT__ ${sanitizeName(test.name)} status=$?"`,
    );
  }
  return parts.join("\n") + "\n";
}

/** Test file: imports the student solution as text + executes assertions. */
function buildTestFile(test: { name: string; code: string }): string {
  return [
    `import { readFileSync } from "node:fs";`,
    `const code = readFileSync("/job/solution.js", "utf8");`,
    `try {`,
    test.code, // the challenge author's assertion snippet
    `  console.log("PASS");`,
    `} catch (err) {`,
    `  console.error(err && err.message ? err.message : String(err));`,
    `  process.exit(1);`,
    `}`,
  ].join("\n");
}

/** Quoted-delimiter heredoc: no interpolation of $ or backticks. */
function heredoc(name: string, content: string): string {
  return `cat > "${name}" << 'CODEJOURNEY_EOF'\n${content}\nCODEJOURNEY_EOF`;
}

function sanitizeName(name: string): string {
  return (
    name
      .toLowerCase()
      .replace(/[^a-z0-9-_]/g, "-")
      .slice(0, 60) || "test"
  );
}
