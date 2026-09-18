import "server-only";

import { createHash, timingSafeEqual } from "node:crypto";

/**
 * Private-beta access gate (Phase 9).
 *
 * When BETA_INVITE_CODE_SHA256 is set (hex-encoded sha-256 of the invite
 * phrase), self-serve registration requires that code. Unset → registration
 * is open (local dev / tests). The code itself lives only in the deployment
 * environment — never in git. Comparison is constant-time against a hash, so
 * neither the code nor a timing oracle leaks, and only the hash needs to be
 * provisioned.
 */
export function betaGateEnabled(): boolean {
  return Boolean(process.env.BETA_INVITE_CODE_SHA256?.trim());
}

/**
 * Verify a submitted invite code. Fails closed: any misconfiguration or an
 * absent/short code is a rejection when the gate is enabled.
 */
export function verifyBetaCode(candidate: unknown): boolean {
  const expectedHex = process.env.BETA_INVITE_CODE_SHA256?.trim().toLowerCase();
  if (!expectedHex || !/^[0-9a-f]{64}$/.test(expectedHex)) return false;
  if (typeof candidate !== "string") return false;
  const trimmed = candidate.trim();
  if (trimmed.length < 6 || trimmed.length > 200) return false;
  const actual = createHash("sha256").update(trimmed, "utf8").digest();
  const expected = Buffer.from(expectedHex, "hex");
  return timingSafeEqual(actual, expected);
}

/** The form field name for the invite code (kept in one place). */
export const BETA_CODE_FIELD = "betaCode";
