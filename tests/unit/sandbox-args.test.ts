import { describe, expect, it } from "vitest";

import { buildDockerArgs } from "@/workers/sandbox";

/**
 * Unit tests for the sandbox docker argument builder (07-10): the hardening
 * set must be complete regardless of host, and SANDBOX_DOCKER_HOST must map
 * to the `-H` daemon flag (dedicated sandbox host, never the web-tier socket).
 */
describe("buildDockerArgs (07-10 sandbox host scoping)", () => {
  const base = {
    memoryMb: 256,
    image: "codejourney-sandbox:latest",
    dockerHost: null,
    name: "cj-sandbox-test",
  };

  it("local mode: no -H flag, full hardening set preserved", () => {
    const args = buildDockerArgs(base);
    expect(args).not.toContain("-H");
    expect(args[0]).toBe("run");
    for (const flag of [
      "--rm",
      "--network",
      "--read-only",
      "--memory",
      "--memory-swap",
      "--cpus",
      "--pids-limit",
      "--cap-drop",
      "--security-opt",
      "--user",
    ]) {
      expect(args).toContain(flag);
    }
    // Specific hardening values:
    expect(args[args.indexOf("--network") + 1]).toBe("none");
    expect(args[args.indexOf("--user") + 1]).toBe("sandbox");
    expect(args[args.indexOf("--cap-drop") + 1]).toBe("ALL");
    expect(args[args.indexOf("--security-opt") + 1]).toBe("no-new-privileges");
    expect(args[args.indexOf("--memory") + 1]).toBe("256m");
    // No swap: memory-swap equals memory.
    expect(args[args.indexOf("--memory-swap") + 1]).toBe("256m");
    // Non-root numeric uid under the cap.
    expect(args[args.indexOf("--pids-limit") + 1]).toBe("64");
    // Image + entrypoint at the end.
    expect(args.at(-2)).toBe("codejourney-sandbox:latest");
    expect(args.at(-1)).toBe("sh");
  });

  it("beta mode: SANDBOX_DOCKER_HOST becomes the first -H daemon flag", () => {
    const args = buildDockerArgs({ ...base, dockerHost: "tcp://sandbox-host:2375" });
    expect(args[0]).toBe("-H");
    expect(args[1]).toBe("tcp://sandbox-host:2375");
    expect(args[2]).toBe("run");
    // Hardening set unchanged when a remote host is targeted.
    expect(args).toContain("--cap-drop");
    expect(args).toContain("--network");
  });

  it("memory ceiling scales with the requested limit", () => {
    const args = buildDockerArgs({ ...base, memoryMb: 512 });
    expect(args[args.indexOf("--memory") + 1]).toBe("512m");
    expect(args[args.indexOf("--memory-swap") + 1]).toBe("512m");
  });
});
