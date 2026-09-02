import { describe, expect, it } from "vitest";

import {
  generateResetToken,
  hashResetToken,
  isResetTokenValid,
  RESET_TOKEN_TTL_MS,
  resetTokenExpiry,
} from "@/lib/auth/reset-token";

describe("password reset tokens (no DB)", () => {
  it("generates url-safe, high-entropy tokens", () => {
    const token = generateResetToken();
    expect(token).toMatch(/^[A-Za-z0-9_-]+$/);
    expect(token.length).toBeGreaterThanOrEqual(40);
    expect(generateResetToken()).not.toBe(token);
  });

  it("hashes deterministically with sha256 (64 hex chars) and never matches the raw token", () => {
    const token = generateResetToken();
    const hash = hashResetToken(token);
    expect(hash).toMatch(/^[a-f0-9]{64}$/);
    expect(hashResetToken(token)).toBe(hash);
    expect(hash).not.toContain(token);
  });

  it("sets expiry one hour out", () => {
    const now = new Date("2026-09-02T12:00:00Z");
    const expiry = resetTokenExpiry(now);
    expect(expiry.getTime() - now.getTime()).toBe(RESET_TOKEN_TTL_MS);
  });

  it("validates rows as unexpired AND unused", () => {
    const now = new Date("2026-09-02T12:00:00Z");
    const valid = {
      expiresAt: new Date(now.getTime() + 1000),
      usedAt: null,
    };
    expect(isResetTokenValid(valid, now)).toBe(true);

    expect(
      isResetTokenValid({ expiresAt: new Date(now.getTime() - 1000), usedAt: null }, now),
    ).toBe(false);
    expect(isResetTokenValid({ expiresAt: new Date(now.getTime() + 1000), usedAt: now }, now)).toBe(
      false,
    );
  });
});
