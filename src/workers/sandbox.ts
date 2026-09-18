import "server-only";

import { randomBytes } from "node:crypto";
import { spawn } from "node:child_process";

import { buildCppJobScript } from "./cpp-runtime";
import { buildCJobScript } from "./c-runtime";
import { buildCSharpJobScript } from "./csharp-runtime";
import { buildJavaJobScript } from "./java-runtime";
import { buildPyJobScript } from "./python-runtime";
import { sanitizeTestName } from "./sanitize-name";

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
  name: string;
}): string[] {
  const args: string[] = [];
  if (options.dockerHost) {
    // Global daemon flag: target the dedicated sandbox host, not the
    // web-tier daemon (07-10). Never a public endpoint.
    args.push("-H", options.dockerHost);
  }
  args.push(
    "run",
    // Container name: the wall-clock timeout (host-side kill) needs to target
    // the CONTAINER — killing the local `docker run` client alone leaves the
    // container running on the daemon indefinitely (leak + CPU burn).
    "--name",
    options.name,
    "--rm", // ephemeral
    "--network",
    "none", // no egress
    "--read-only", // immutable rootfs
    "--tmpfs",
    // /tmp allows exec (Docker's tmpfs defaults include noexec, so it must
    // be explicit): the C++ track compiles test binaries there. This is NOT
    // a weakening — arbitrary student code already executes in-container via
    // the node/python interpreters (which noexec never prevented); the real
    // boundaries are network-off, read-only rootfs, cap-drop ALL, non-root,
    // and the memory/cpu/pids ceilings below. nosuid/nodev stay.
    "/tmp:size=64m,exec,nosuid,nodev",
    "--tmpfs",
    "/job:size=16m,noexec,nosuid,nodev,uid=100,gid=101", // job files (data only)
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
 * Best-effort container kill (Phase 9 leak fix): on wall-clock timeout or
 * client death we must stop the CONTAINER, not just the local docker CLI
 * process. `--rm` then cleans it up daemon-side. Failures are swallowed:
 * cleanup is best-effort and a leaked container is logged by the caller.
 */
export function killSandboxContainer(name: string, dockerHost: string | null): void {
  const args: string[] = [];
  if (dockerHost) args.push("-H", dockerHost);
  args.push("kill", name);
  try {
    const kill = spawn("docker", args, {
      stdio: "ignore",
      env: {
        PATH: process.env.PATH ?? "/usr/local/bin:/usr/bin:/bin",
        HOME: "/tmp",
        NODE_ENV: process.env.NODE_ENV,
      } as NodeJS.ProcessEnv,
    });
    kill.on("error", () => undefined);
    // Do not await: the docker run client is being torn down anyway.
    kill.unref();
  } catch {
    // best-effort by contract
  }
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
  /** "python" runs solution.py with the Python harness; "cpp" compiles
   *  solution.cpp with the C++ harness; "java" compiles Solution.java with
   *  the Java harness; "c" compiles solution.c with the C harness
   *  (c-runtime.ts); "csharp" compiles Solution.cs with the C# harness
   *  (csharp-runtime.ts); default "javascript". */
  language?: "javascript" | "python" | "cpp" | "java" | "c" | "csharp";
}): Promise<SandboxResult> {
  const timeoutMs = Math.min(Math.max(options.timeoutMs, 1000), MAX_TIMEOUT_MS);
  const delim = randomDelimiter();
  // Unique container name (unique-ify with the same entropy as the delimiter).
  const containerName = `cj-sandbox-${randomBytes(8).toString("hex")}`;
  // Defensive: if the submitted code/tests happen to contain the delimiter,
  // fail closed rather than risk the heredoc being terminated inside sh.
  const collides = [options.code, ...options.testFiles.map((t) => t.code), STUBS_MODULE].some((s) =>
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
    // stdin. Language branches ONLY the job script (solution.py + python3
    // tests vs solution.js + node tests) — hardening, delimiter hygiene,
    // timeout, and marker protocol are identical for every language.
    // the command. Files are written to tmpfs (world-writable, ephemeral);
    // code and tests are passed as argv-safe heredoc content via stdin.
    const script = buildJobScript(options.code, options.testFiles, delim, options.language ?? "javascript");

    const args = buildDockerArgs({
      memoryMb: options.memoryMb,
      image: SANDBOX_IMAGE,
      dockerHost: SANDBOX_DOCKER_HOST,
      name: containerName,
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
      // Kill the container FIRST (the actual workload), then the client.
      // Client-only kill leaves the container running on the daemon forever.
      killSandboxContainer(containerName, SANDBOX_DOCKER_HOST);
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
      killSandboxContainer(containerName, SANDBOX_DOCKER_HOST);
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
  language: "javascript" | "python" | "cpp" | "java" | "c" | "csharp" = "javascript",
): string {
  if (language === "python") {
    return buildPyJobScript({ code, testFiles }, delim);
  }
  if (language === "cpp") {
    return buildCppJobScript({ code, testFiles }, delim);
  }
  if (language === "c") {
    return buildCJobScript({ code, testFiles }, delim);
  }
  if (language === "java") {
    return buildJavaJobScript({ code, testFiles }, delim);
  }
  if (language === "csharp") {
    return buildCSharpJobScript({ code, testFiles }, delim);
  }
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("solution.js", code, delim));
  // Challenge globals (button/display/storage/fake fetch/…): the QA harness
  // provides these to every test run; without them the DOM/async/storage
  // challenges' tests throw ReferenceError in the real sandbox even for a
  // correct solution. Fresh per test file (each test file is its own
  // `node` process, so the module-level state never leaks between tests).
  parts.push(heredoc("stubs.mjs", STUBS_MODULE, delim));
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
    // Challenge-provided globals (same contract as the QA harness).
    `import "./stubs.mjs";`,
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

// Diacritic-preserving shared sanitizer (Vietnamese test names stay
// readable in the verdict panel; learner bug report 2026-09-13).
function sanitizeName(name: string): string {
  return sanitizeTestName(name);
}

/**
 * Challenge-provided globals, injected into every test file's process
 * (same contract as the content QA harness's buildStubs). A lightweight
 * DOM element recorder covers the DOM/storage/async challenges' tests.
 * Declared with `var` + globalThis assignment so bare references inside
 * author snippets resolve as globals.
 */
const STUBS_MODULE = String.raw`
function makeEl(tag = "div") {
  const e = {
    tagName: String(tag).toUpperCase(),
    textContent: "",
    className: "",
    src: "",
    alt: "",
    value: "",
    children: [],
    listeners: {},
    classList: {
      add: (...c) => c.forEach((x) => e._added.add(x)),
      remove: () => {},
      toggle: () => {},
    },
    _added: new Set(),
    addEventListener: (type, fn) => (e.listeners[type] = fn),
    appendChild: (c) => e.children.push(c),
    remove: () => {},
  };
  return e;
}
const __listEl = makeEl("ul");
const __storageMap = new Map();

var api = {
  loadUser: () => Promise.resolve({ name: "Ada" }),
  loadGreeting: (n) => Promise.resolve("Hello, " + n),
};
// NOTE: fetch is intentionally NOT stubbed — Node's native fetch stays, and
// --network none makes it unable to reach out. Tests that need a fake
// fetch provide one explicitly (e.g. as a new Function parameter).
var checkReady = () => Promise.resolve(true);
var storage = {
  setItem: (k, v) => __storageMap.set(String(k), String(v)),
  getItem: (k) => (__storageMap.has(String(k)) ? __storageMap.get(String(k)) : null),
  removeItem: (k) => __storageMap.delete(String(k)),
};
var document = {
  createElement: (t) => makeEl(t),
  querySelector: (sel) =>
    String(sel).includes("task-list") || String(sel).includes("todo-list") ? __listEl : makeEl("div"),
  getElementById: () => __listEl,
};
var button = makeEl("button");
var display = makeEl("span");
var heading = makeEl("h1");
var intro = makeEl("p");
var hero = makeEl("img");
var form = makeEl("form");
var usernameInput = makeEl("input");
var emailInput = makeEl("input");
var errorBox = makeEl("div");

// Bare button/display/... references inside new Function(code) bodies
// resolve through the global scope only if they are true globals.
for (const [k, v] of Object.entries({
  api,
  checkReady,
  storage,
  document,
  button,
  display,
  heading,
  intro,
  hero,
  form,
  usernameInput,
  emailInput,
  errorBox,
})) {
  globalThis[k] = v;
}
`;
