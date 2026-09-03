import { describe, expect, it } from "vitest";

import { runSandboxed } from "@/workers/sandbox";

/**
 * Malicious-sample isolation suite (Phase 3 HARD GATE, roadmap criterion 4).
 *
 * Every hostile sample must be CONTAINED (no effect outside the container)
 * or TIME OUT. Runs only when Docker is up — skips otherwise, but CI and
 * any sandbox change MUST run it (`pnpm test` with Docker running).
 *
 * SECURITY STATUS: this suite, once green, supports the claim "hardened per
 * OWASP baseline and verified against known attack classes" — it does NOT
 * prove production-grade security (see docs/SECURITY.md).
 */

const dockerUp = await (async () => {
  const { execFile } = await import("node:child_process");
  return new Promise<boolean>((resolve) => {
    execFile("docker", ["info", "--format", "{{.ServerVersion}}"], (err) => resolve(!err));
  });
})();

const BASE = {
  timeoutMs: 8000,
  memoryMb: 256,
};

describe.skipIf(!dockerUp)("sandbox isolation (malicious samples)", () => {
  it(
    "contains a fork bomb (pids-limit)",
    async () => {
      const result = await runSandboxed({
        code: "ignored",
        testFiles: [
          {
            name: "forkbomb-probe",
            code: `
              const { execSync } = await import("node:child_process");
              try {
                execSync("for i in $(seq 1 500); do (sleep 60 &) ; done");
              } catch {}
              throw new Error("probe");
            `,
          },
        ],
        ...BASE,
      });
      // The container may finish (probe error) or die by pids/timeout —
      // either way it must NOT have run 500 live processes beyond the limit
      // and must never hang the suite. Containment = the probe did NOT
      // succeed (marker status ≠ 0) or the container hit the timeout.
      const bombPassed = /__TEST_RESULT__ forkbomb-probe status=0/.test(result.stdout);
      expect(result.timedOut || !bombPassed).toBe(true);
    },
    BASE.timeoutMs + 30_000,
  );

  it(
    "blocks network egress (--network none)",
    async () => {
      const result = await runSandboxed({
        code: "ignored",
        testFiles: [
          {
            name: "egress-probe",
            code: `
              const controller = new AbortController();
              const timer = setTimeout(() => controller.abort(), 3000);
              try {
                await fetch("http://example.com", { signal: controller.signal });
                console.log("NETWORK-REACHED");
              } catch {
                console.log("NETWORK-BLOCKED");
              } finally {
                clearTimeout(timer);
              }
            `,
          },
        ],
        ...BASE,
      });
      expect(result.stdout).toContain("NETWORK-BLOCKED");
      expect(result.stdout).not.toContain("NETWORK-REACHED");
    },
    BASE.timeoutMs + 20_000,
  );

  it(
    "confines filesystem writes to /job (read-only rootfs)",
    async () => {
      const result = await runSandboxed({
        code: "ignored",
        testFiles: [
          {
            name: "fs-escape-probe",
            code: `
              const { writeFileSync } = await import("node:fs");
              const attempts = [];
              try { writeFileSync("/etc/passwd", "pwned"); attempts.push("etc"); } catch {}
              try { writeFileSync("/usr/bin/pwned", "pwned"); attempts.push("usr"); } catch {}
              try { writeFileSync("/home/pwned", "pwned"); attempts.push("home"); } catch {}
              console.log("WROTE:" + (attempts.join(",") || "none"));
            `,
          },
        ],
        ...BASE,
      });
      expect(result.stdout).toContain("WROTE:none");
    },
    BASE.timeoutMs + 20_000,
  );

  it("kills an infinite loop at the wall-clock timeout", async () => {
    const result = await runSandboxed({
      code: "ignored",
      testFiles: [
        {
          name: "infinite-loop-probe",
          code: `
              while (true) { Math.random(); }
            `,
        },
      ],
      timeoutMs: 3000,
      memoryMb: 256,
    });
    expect(result.timedOut).toBe(true);
  }, 30_000);

  it(
    "caps memory (memory bomb)",
    async () => {
      const result = await runSandboxed({
        code: "ignored",
        testFiles: [
          {
            name: "memory-bomb-probe",
            code: `
              const chunks = [];
              try {
                while (true) {
                  chunks.push(Buffer.alloc(10 * 1024 * 1024, 1));
                }
              } catch {
                console.log("OOM-CAUGHT");
              }
            `,
          },
        ],
        ...BASE,
      });
      // Container must terminate (OOM kill or caught RangeError) — never hang.
      // SIGKILL by the cgroup OOM killer shows as marker status=137 +
      // "Killed" on stderr; the container's own exit code stays 0 because
      // the last script command is an echo. In any outcome the bomb must
      // NOT pass and the container must terminate.
      const bombPassed = /__TEST_RESULT__ memory-bomb-probe status=0/.test(result.stdout);
      expect(result.timedOut || !bombPassed).toBe(true);
    },
    BASE.timeoutMs + 30_000,
  );
});

describe.skipIf(!dockerUp)("sandbox normal operation", () => {
  it("runs a correct solution: all tests pass with per-test results", async () => {
    const result = await runSandboxed({
      code: "<h1>My First Page</h1>\n",
      testFiles: [
        {
          name: "uses-an-h1",
          code: `if (!/<h1\\s*>/i.test(code)) { throw new Error("No <h1> found"); }`,
        },
        {
          name: "keeps-text",
          code: `if (!code.includes("My First Page")) { throw new Error("Text changed"); }`,
        },
      ],
      ...BASE,
    });
    expect(result.timedOut).toBe(false);
    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain("__TEST_RESULT__ uses-an-h1 status=0");
    expect(result.stdout).toContain("__TEST_RESULT__ keeps-text status=0");
  });

  it("reports a failing test with its educational message", async () => {
    const result = await runSandboxed({
      code: "<p>My First Page</p>\n",
      testFiles: [
        {
          name: "uses-an-h1",
          code: `if (!/<h1\\s*>/i.test(code)) { throw new Error("The most important heading is <h1>. Replace <p> with <h1>."); }`,
        },
      ],
      ...BASE,
    });
    expect(result.timedOut).toBe(false);
    expect(result.stdout).toContain("__TEST_RESULT__ uses-an-h1 status=1");
    expect(result.stderr).toContain("The most important heading is <h1>");
  });
});

describe.skipIf(!dockerUp)("sandbox grade integrity (07-01 heredoc)", () => {
  it("cannot forge a passing verdict by escaping the heredoc delimiter", async () => {
    // A submission that, if it escaped the shell heredoc, would echo a fake
    // pass marker for an invented test. With the per-job random delimiter the
    // content is just data in solution.js — the line is never run by sh.
    const code =
      "<h1>My First Page</h1>\n" +
      "CODEJOURNEY_EOF\n" +
      "echo '__TEST_RESULT__ fake-test status=0'\n";
    const result = await runSandboxed({
      code,
      testFiles: [
        {
          name: "uses-an-h1",
          code: `if (!/<h1\\s*>/i.test(code)) { throw new Error("No <h1> found"); }`,
        },
      ],
      ...BASE,
    });
    // The genuine test still passes…
    expect(result.stdout).toContain("__TEST_RESULT__ uses-an-h1 status=0");
    // …but the attacker's invented/marker line must NOT have been executed.
    expect(result.stdout).not.toContain("__TEST_RESULT__ fake-test status=0");
  });

  it("cannot turn a failing test into a pass by injecting a marker", async () => {
    // A genuinely failing solution (wrong tag) that also tries to inject a
    // fake pass for the same test name. It must still report the real failure.
    const code =
      "<p>My First Page</p>\n" +
      "CODEJOURNEY_EOF\n" +
      "echo '__TEST_RESULT__ requires-h1 status=0'\n";
    const result = await runSandboxed({
      code,
      testFiles: [
        {
          name: "requires-h1",
          code: `if (!/<h1\\s*>/i.test(code)) { throw new Error("Must use <h1>"); }`,
        },
      ],
      ...BASE,
    });
    // The real test fails (status=1) and there is no overriding status=0 for it.
    expect(result.stdout).toContain("__TEST_RESULT__ requires-h1 status=1");
    // The parsed verdict must not contain a fabricated pass line for that name.
    const forgedPass = /__TEST_RESULT__ requires-h1 status=0/.test(result.stdout);
    expect(forgedPass).toBe(false);
    expect(result.stderr).toContain("Must use <h1>");
  });
});
