import "server-only";

import { randomBytes } from "node:crypto";
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
 * SECURITY STATUS: hardened per baseline; explicitly scoped to LOCAL and
 * PRIVATE BETA (beta: dedicated sandbox host via SANDBOX_DOCKER_HOST, never
 * the web-tier daemon). NOT claimed production-grade — public production
 * migrates to self-hosted Judge0 per docs/PRODUCTION.md (docs/SECURITY.md
 * honesty rule).
 */

const SANDBOX_IMAGE = process.env.SANDBOX_IMAGE ?? "codejourney-sandbox:latest";
/**
 * Sandbox host (07-10 environment split): unset → the local Docker daemon
 * (development/tests). In private beta this points at a DEDICATED sandbox
 * worker host (e.g. tcp://sandbox-host:2375) so the web tier never holds a
 * Docker socket — socket access is host-level privilege. The worker must be
 * the only client of that endpoint and must carry no user-data credentials.
 * Public production migrates execution to self-hosted Judge0 (docs/PRODUCTION.md).
 */
const SANDBOX_DOCKER_HOST = process.env.SANDBOX_DOCKER_HOST?.trim() || null;
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

/**
 * The full docker argument vector for a sandboxed run. Exported pure (07-10)
 * so tests can assert the hardening set and host isolation without Docker.
 */
export function buildDockerArgs(options: {
  memoryMb: number;
  image: string;
  dockerHost: string | null;
}): string[] {
  const args: string[] = [];
  if (options.dockerHost) {
    // Global daemon flag: target the dedicated sandbox host, not the
    // web-tier daemon (07-10). Never a public endpoint.
    args.push("-H", options.dockerHost);
  }
  args.push(
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
    options.image,
    "sh", // reads the script from stdin
  );
  return args;
}

/**
 * Per-job heredoc delimiter (07-01 grade integrity). The submitted code and
 * test snippets are written into the job script as heredoc data. A FIXED
 * delimiter lets a submission containing it terminate the heredoc early and
 * inject shell commands — which could echo forged ``__TEST_RESULT__`` markers
 * and produce a false passing verdict. A fresh 96-bit random delimiter per
 * job makes that impossible (the attacker cannot predict it), and we also
 * reject any content that collides with the chosen delimiter before running.
 */
function randomDelimiter(): string {
  return "CJ_EOF_" + randomBytes(12).toString("hex");
}

export function runSandboxed(options: {
  code: string;
  testFiles: { name: string; code: string }[];
  timeoutMs: number;
  memoryMb: number;
}): Promise<SandboxResult> {
  const timeoutMs = Math.min(Math.max(options.timeoutMs, 1000), MAX_TIMEOUT_MS);
  const delim = randomDelimiter();
  // Defensive: if the submitted code/tests happen to contain the delimiter,
  // fail closed rather than risk the heredoc being terminated inside sh.
  const collides = [options.code, ...options.testFiles.map((t) => t.code)].some((s) =>
    s.includes(delim),
  );
  if (collides) {
    return Promise.resolve({
      timedOut: false,
      exitCode: 1,
      stdout: "",
      stderr: "Rejected: submitted code collides with the per-job delimiter.",
    });
  }
  return new Promise((resolve, reject) => {
    // Materialize files into a docker-build-compatible context via stdin:
    // we create the job dir in-container through a shell script passed as
    // the command. Files are written to tmpfs (world-writable, ephemeral);
    // code and tests are passed as argv-safe heredoc content via stdin.
    const script = buildJobScript(options.code, options.testFiles, delim);

    const args = buildDockerArgs({
      memoryMb: options.memoryMb,
      image: SANDBOX_IMAGE,
      dockerHost: SANDBOX_DOCKER_HOST,
    });

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
 * (tmpfs) and runs them with node. Heredocs with a per-job random quoted
 * delimiter mean NO shell expansion AND no predictable escape — student code
 * is data, never interpreted by sh.
 */
function buildJobScript(
  code: string,
  testFiles: { name: string; code: string }[],
  delim: string,
): string {
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("solution.js", code, delim));
  for (const test of testFiles) {
    parts.push(heredoc(`test-${sanitizeName(test.name)}.mjs`, buildTestFile(test), delim));
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
function heredoc(name: string, content: string, delim: string): string {
  return `cat > "${name}" << '${delim}'\n${content}\n${delim}`;
}

function sanitizeName(name: string): string {
  return (
    name
      .toLowerCase()
      .replace(/[^a-z0-9-_]/g, "-")
      .slice(0, 60) || "test"
  );
}
