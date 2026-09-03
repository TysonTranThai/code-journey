import { randomUUID } from "node:crypto";

import { describe, expect, it } from "vitest";

import { db } from "@/lib/db";
import { MENTOR_LIMITS, checkMentorQuota } from "@/lib/mentor/rate-limit";

const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

/**
 * Mentor quota now uses the atomic `consume` counter (07-03), so `remaining`
 * reflects the count AFTER this request. Each test uses a fresh userId so the
 * per-user counter starts empty.
 */
describe.skipIf(!dbUp)("mentor rate limiting (AI-03, atomic)", () => {
  it("allows under the daily limit and reports remaining post-increment", async () => {
    const userId = randomUUID();
    const first = await checkMentorQuota(userId, "hintsPerDay");
    expect(first.allowed).toBe(true);
    expect(first.remaining).toBe(MENTOR_LIMITS.hintsPerDay - 1);

    const second = await checkMentorQuota(userId, "hintsPerDay");
    expect(second.remaining).toBe(MENTOR_LIMITS.hintsPerDay - 2);
  });

  it("blocks when the daily limit is exhausted", async () => {
    const userId = randomUUID();
    let last;
    for (let i = 0; i < MENTOR_LIMITS.hintsPerDay; i++) {
      last = await checkMentorQuota(userId, "hintsPerDay");
      expect(last.allowed).toBe(true);
    }
    expect(last!.remaining).toBe(0);

    const over = await checkMentorQuota(userId, "hintsPerDay");
    expect(over.allowed).toBe(false);
    expect(over.remaining).toBe(0);
  });

  it("tracks kinds independently (explains have their own counter)", async () => {
    const userId = randomUUID();
    for (let i = 0; i < MENTOR_LIMITS.hintsPerDay + 1; i++) {
      await checkMentorQuota(userId, "hintsPerDay");
    }
    const hints = await checkMentorQuota(userId, "hintsPerDay");
    expect(hints.allowed).toBe(false);

    const explains = await checkMentorQuota(userId, "explainsPerDay");
    expect(explains.allowed).toBe(true);
    expect(explains.remaining).toBe(MENTOR_LIMITS.explainsPerDay - 1);
  });
});
