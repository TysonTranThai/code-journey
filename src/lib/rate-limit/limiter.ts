import "server-only";

import { sql } from "drizzle-orm";
import { headers } from "next/headers";

import { db } from "@/lib/db";
import { rateLimitEvents } from "@/lib/db/schema";

/**
 * Atomic database-backed rate limiter (07-03).
 *
 * Fixed-window counter keyed by `scope:key:window-bucket`. The count is
 * incremented ON CONFLICT in a single statement, so check-and-increment is one
 * atomic operation — no TOCTOU race. Suitable for beta: no new infra, no
 * vendor lock-in. Behind this interface a Redis/upstash store can be swapped in
 * for distributed deployment without changing call sites.
 *
 * Endpoints call `consume(...)` and return 429 (with Retry-After) when it is
 * not allowed. `clientIp()` derives the caller IP from proxy headers.
 */

export const HOUR_MS = 3_600_000;
export const MINUTE_MS = 60_000;
export const DAY_MS = 86_400_000;

export interface ConsumeResult {
  allowed: boolean;
  /** Requests remaining in the current window (>= 0). */
  remaining: number;
  /** Milliseconds until the current window resets (for Retry-After). */
  resetMs: number;
}

/**
 * Atomically record a request for `scope:key` within `windowMs` and report
 * whether it is within `limit`. Increments the counter in the same statement
 * that checks it.
 */
export async function consume(
  scope: string,
  key: string,
  limit: number,
  windowMs: number,
): Promise<ConsumeResult> {
  const now = Date.now();
  const bucket = Math.floor(now / windowMs);
  const windowStart = bucket * windowMs;
  const pk = `${scope}:${key}:${bucket}`;

  // Single atomic upsert: insert at count 1, or on conflict increment +1.
  const [row] = await db
    .insert(rateLimitEvents)
    .values({
      key: pk,
      count: 1,
      windowStart: new Date(windowStart),
      expiresAt: new Date(windowStart + windowMs),
    })
    .onConflictDoUpdate({
      target: rateLimitEvents.key,
      set: { count: sql`${rateLimitEvents.count} + 1` },
    })
    .returning({ count: rateLimitEvents.count });

  const count = row?.count ?? 1;
  return {
    allowed: count <= limit,
    remaining: Math.max(0, limit - count),
    resetMs: Math.max(0, windowStart + windowMs - now),
  };
}

/** Derive the caller IP from proxy headers (best-effort; falls back to "unknown"). */
export async function clientIp(): Promise<string> {
  const h = await headers();
  const fwd = h.get("x-forwarded-for");
  if (fwd) return fwd.split(",")[0]!.trim();
  return h.get("x-real-ip") ?? "unknown";
}

/** A friendly message + Retry-After header value for an exhausted limit. */
export function retryMessage(resetMs: number): { message: string; retryAfterSec: number } {
  const sec = Math.max(1, Math.ceil(resetMs / 1000));
  return {
    message: `Too many requests. Try again in ${sec}s.`,
    retryAfterSec: sec,
  };
}
