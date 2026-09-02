import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { eq, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import { mentorRequests, users } from "@/lib/db/schema";
import { MENTOR_LIMITS, checkMentorQuota, recordMentorRequest } from "@/lib/mentor/rate-limit";

const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

describe.skipIf(!dbUp)("mentor rate limiting (AI-03)", () => {
  const email = "mentor-quota-test@codejourney.local";
  let userId: string;

  beforeAll(async () => {
    const [user] = await db
      .insert(users)
      .values({ email, name: "Mentor Quota Test" })
      .onConflictDoUpdate({ target: users.email, set: { name: "Mentor Quota Test" } })
      .returning();
    userId = user!.id;
    await db.delete(mentorRequests).where(eq(mentorRequests.userId, userId));
  });

  afterAll(async () => {
    await db.delete(mentorRequests).where(eq(mentorRequests.userId, userId));
    await db.delete(users).where(sql`${users.email} = ${email}`);
  });

  it("allows requests under the daily limit and counts remaining", async () => {
    const first = await checkMentorQuota(userId, "hintsPerDay");
    expect(first.allowed).toBe(true);
    expect(first.remaining).toBe(MENTOR_LIMITS.hintsPerDay);

    await recordMentorRequest(userId, "hintsPerDay");
    const after = await checkMentorQuota(userId, "hintsPerDay");
    expect(after.remaining).toBe(MENTOR_LIMITS.hintsPerDay - 1);
  });

  it("blocks when the daily limit is exhausted", async () => {
    // Fill the rest of the quota.
    const toInsert = MENTOR_LIMITS.hintsPerDay;
    for (let i = 0; i < toInsert; i++) {
      await recordMentorRequest(userId, "hintsPerDay");
    }
    const exhausted = await checkMentorQuota(userId, "hintsPerDay");
    expect(exhausted.allowed).toBe(false);
    expect(exhausted.remaining).toBe(0);
  });

  it("tracks kinds independently (explains have their own counter)", async () => {
    const explains = await checkMentorQuota(userId, "explainsPerDay");
    expect(explains.allowed).toBe(true);
    expect(explains.remaining).toBe(MENTOR_LIMITS.explainsPerDay);
  });
});
