import { createHash } from "node:crypto";
import { afterEach, describe, expect, it } from "vitest";

import { BETA_CODE_FIELD, betaGateEnabled, verifyBetaCode } from "@/lib/beta/access";

/**
 * Private-beta access gate (Phase 9): the invite code must be verified
 * against its sha-256 hash, fail closed on any misconfiguration, and be
 * env-gated so local dev/tests keep open registration.
 */
describe("beta access gate", () => {
  afterEach(() => {
    delete process.env.BETA_INVITE_CODE_SHA256;
  });

  it("is disabled when no hash is configured", () => {
    expect(betaGateEnabled()).toBe(false);
    expect(verifyBetaCode("anything")).toBe(false);
  });

  it("accepts the correct code and rejects wrong ones (constant-time path)", () => {
    const real = "test-invite-code";
    process.env.BETA_INVITE_CODE_SHA256 = createHash("sha256").update(real, "utf8").digest("hex");

    expect(betaGateEnabled()).toBe(true);
    expect(verifyBetaCode(real)).toBe(true);
    expect(verifyBetaCode("wrong-guess")).toBe(false);
    expect(verifyBetaCode("")).toBe(false);
    expect(verifyBetaCode(undefined)).toBe(false);
    expect(verifyBetaCode(12345)).toBe(false);
    // Whitespace around a valid code is tolerated (form input).
    expect(verifyBetaCode(`  ${real}  `)).toBe(true);
  });

  it("fails closed on a malformed configured hash", () => {
    process.env.BETA_INVITE_CODE_SHA256 = "not-a-hash";
    expect(verifyBetaCode("anything")).toBe(false);
  });

  it("keeps the form field name stable", () => {
    expect(BETA_CODE_FIELD).toBe("betaCode");
  });
});
