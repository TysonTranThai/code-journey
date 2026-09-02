import { afterAll, beforeAll, describe, expect, it } from "vitest";

import { db } from "@/lib/db";
import { users, achievements, progressEvents, submissions } from "@/lib/db/schema";
import { getAchievementDefs } from "@/lib/progress/achievement-defs";
import {
  maybeAwardAchievements,
  ProgressVerificationError,
  recordChallengeCompletion,
  recordLessonCompletion,
} from "@/lib/progress/recording";
import { eq, sql } from "drizzle-orm";

describe("achievement definitions (content-as-data)", () => {
  it("validates the shipped achievements.json with unique slugs", () => {
    const defs = getAchievementDefs();
    expect(defs.length).toBeGreaterThanOrEqual(5);
    const ids = defs.map((d) => d.id);
    expect(new Set(ids).size).toBe(ids.length);
    expect(defs.map((d) => d.id)).toContain("first-lesson");
  });
});

const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

describe.skipIf(!dbUp)("achievement awarding (DB-gated)", () => {
  const testEmail = "achievements-test@codejourney.local";
  let userId: string;

  beforeAll(async () => {
    const [user] = await db
      .insert(users)
      .values({ email: testEmail, name: "Achievement Test" })
      .onConflictDoUpdate({
        target: users.email,
        set: { name: "Achievement Test" },
      })
      .returning();
    userId = user!.id;
    await db.delete(progressEvents).where(eq(progressEvents.userId, userId));
    await db.delete(achievements).where(eq(achievements.userId, userId));
  });

  afterAll(async () => {
    await db.delete(progressEvents).where(eq(progressEvents.userId, userId));
    await db.delete(achievements).where(eq(achievements.userId, userId));
    await db.delete(users).where(sql`${users.email} = ${testEmail}`);
  });

  it("awards first-lesson after one lesson event", async () => {
    await db.insert(progressEvents).values({
      userId,
      contentType: "lesson",
      contentId: "introduction-to-html",
    });
    const awarded = await maybeAwardAchievements(userId);
    expect(awarded).toContain("first-lesson");
  });

  it("is idempotent: re-evaluation does not duplicate awards", async () => {
    const again = await maybeAwardAchievements(userId);
    expect(again).not.toContain("first-lesson");
    const rows = await db
      .select()
      .from(achievements)
      .where(eq(achievements.userId, userId));
    expect(rows.filter((r) => r.achievementId === "first-lesson")).toHaveLength(1);
  });

  it("awards five-lessons at the threshold", async () => {
    const ids = ["html-elements", "html-attributes", "html-links", "html-images"];
    for (const contentId of ids) {
      await db
        .insert(progressEvents)
        .values({ userId, contentType: "lesson", contentId })
        .onConflictDoNothing();
    }
    const awarded = await maybeAwardAchievements(userId);
    expect(awarded).toContain("five-lessons");
  });

  it("awards first-challenge from a recorded challenge completion", async () => {
    await recordChallengeCompletion(userId, "fix-the-heading");
    const rows = await db
      .select()
      .from(achievements)
      .where(eq(achievements.userId, userId));
    expect(rows.some((r) => r.achievementId === "first-challenge")).toBe(true);
    // And the event exists exactly once.
    const events = await db
      .select()
      .from(progressEvents)
      .where(eq(progressEvents.userId, userId));
    expect(
      events.filter(
        (e) => e.contentType === "challenge" && e.contentId === "fix-the-heading",
      ),
    ).toHaveLength(1);
  });
});

describe.skipIf(!dbUp)("lesson completion verification (PROG-02)", () => {
  const testEmail = "lesson-verify-test@codejourney.local";
  let userId: string;

  beforeAll(async () => {
    const [user] = await db
      .insert(users)
      .values({ email: testEmail, name: "Lesson Verify Test" })
      .onConflictDoUpdate({
        target: users.email,
        set: { name: "Lesson Verify Test" },
      })
      .returning();
    userId = user!.id;
    await db.delete(progressEvents).where(eq(progressEvents.userId, userId));
    await db.delete(submissions).where(eq(submissions.userId, userId));
  });

  afterAll(async () => {
    await db.delete(progressEvents).where(eq(progressEvents.userId, userId));
    await db.delete(submissions).where(eq(submissions.userId, userId));
    await db.delete(users).where(sql`${users.email} = ${testEmail}`);
  });

  it("rejects completion of a lesson whose challenge was never passed", async () => {
    await expect(
      recordLessonCompletion(
        userId,
        "web-development",
        "web-development-foundations",
        "html-foundations",
        "introduction-to-html",
      ),
    ).rejects.toBeInstanceOf(ProgressVerificationError);
  });

  it("records completion once the challenge has a passing submission (idempotent)", async () => {
    await db.insert(submissions).values({
      userId,
      challengeId: "fix-the-heading",
      code: "<h1>x</h1>",
      verdict: "passed",
    });
    const first = await recordLessonCompletion(
      userId,
      "web-development",
      "web-development-foundations",
      "html-foundations",
      "introduction-to-html",
    );
    expect(first.recorded).toBe(true);

    const second = await recordLessonCompletion(
      userId,
      "web-development",
      "web-development-foundations",
      "html-foundations",
      "introduction-to-html",
    );
    expect(second.recorded).toBe(false); // idempotent

    const events = await db
      .select()
      .from(progressEvents)
      .where(
        sql`${progressEvents.userId} = ${userId} and ${progressEvents.contentId} = 'introduction-to-html'`,
      );
    expect(events).toHaveLength(1);
  });

  it("records lessons without challenges freely (viewing completion)", async () => {
    const result = await recordLessonCompletion(
      userId,
      "web-development",
      "web-development-foundations",
      "html-foundations",
      "html-elements",
    );
    expect(result.recorded).toBe(true);
  });
});
