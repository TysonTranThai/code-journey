import { randomUUID } from "node:crypto";

import { describe, expect, it } from "vitest";

import { db } from "@/lib/db";
import { consume, MINUTE_MS } from "@/lib/rate-limit/limiter";

const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

describe.skipIf(!dbUp)("rate limiter consume (07-03)", () => {
  it("counts up to the limit then blocks, with remaining and reset", async () => {
    const key = `rt-${randomUUID()}`;
    for (let i = 1; i <= 3; i++) {
      const r = await consume("itest", key, 3, MINUTE_MS);
      expect(r.allowed).toBe(true);
      expect(r.remaining).toBe(3 - i);
      expect(r.resetMs).toBeGreaterThan(0);
    }
    const over = await consume("itest", key, 3, MINUTE_MS);
    expect(over.allowed).toBe(false);
    expect(over.remaining).toBe(0);
  });

  it("counts independently per scope+key", async () => {
    const a = `rt-${randomUUID()}`;
    const b = `rt-${randomUUID()}`;
    await consume("itest", a, 5, MINUTE_MS);
    const a2 = await consume("itest", a, 5, MINUTE_MS);
    const b1 = await consume("itest", b, 5, MINUTE_MS);
    expect(a2.remaining).toBe(3);
    expect(b1.remaining).toBe(4);
  });

  it("is atomic under concurrency (never over-counts an allowed call)", async () => {
    const key = `rt-${randomUUID()}`;
    const limit = 5;
    const results = await Promise.all(
      Array.from({ length: 10 }, () => consume("itest", key, limit, MINUTE_MS)),
    );
    // With a non-atomic read-then-write, concurrent calls could all read count <
    // limit and overshoot. The atomic upsert ensures exactly `limit` succeed.
    const allowed = results.filter((r) => r.allowed).length;
    expect(allowed).toBe(limit);
  });
});
