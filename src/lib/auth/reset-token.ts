import { createHash, randomBytes } from "node:crypto";

/**
 * Password reset token mechanics (decision D-06).
 *
 * Raw tokens are shown once (in dev: logged to the server console) and are
 * NEVER stored — only their sha256 hex digest. Tokens are single-use
 * (usedAt) and expire after one hour.
 */

export const RESET_TOKEN_TTL_MS = 60 * 60 * 1000; // 1 hour

/** 32 random bytes, url-safe base64 — the value the user clicks. */
export function generateResetToken(): string {
  return randomBytes(32).toString("base64url");
}

/** sha256 hex digest — the only form ever persisted. */
export function hashResetToken(rawToken: string): string {
  return createHash("sha256").update(rawToken).digest("hex");
}

export function resetTokenExpiry(from: Date = new Date()): Date {
  return new Date(from.getTime() + RESET_TOKEN_TTL_MS);
}

/** True when the stored row is still clickable (unexpired, unused). */
export function isResetTokenValid(
  row: {
    expiresAt: Date;
    usedAt: Date | null;
  },
  now: Date = new Date(),
): boolean {
  return row.usedAt === null && row.expiresAt.getTime() > now.getTime();
}
