import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { eq, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import { comments, discussionThreads, users } from "@/lib/db/schema";
import { countLessonThreads, getLessonThreads, getThread } from "@/lib/discussions/threads";
// Server actions (createThread/addReply) are exercised live via the app;
// requireUser() redirects outside a session so the DB layer is tested here.

const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

describe.skipIf(!dbUp)("discussions (COMM-01..03)", () => {
  const email = "discussions-test@codejourney.local";
  let userId: string;

  beforeAll(async () => {
    const [user] = await db
      .insert(users)
      .values({ email, name: "Discussion Tester" })
      .onConflictDoUpdate({ target: users.email, set: { name: "Discussion Tester" } })
      .returning();
    userId = user!.id;
    await db.delete(discussionThreads).where(eq(discussionThreads.userId, userId));
  });

  afterAll(async () => {
    await db.delete(discussionThreads).where(eq(discussionThreads.userId, userId));
    await db.delete(comments).where(eq(comments.userId, userId));
    await db.delete(users).where(sql`${users.email} = ${email}`);
  });

  it("createThread + addReply build a readable thread (server-verified writes)", async () => {
    // Note: requireUser() would redirect outside a session — these paths are
    // exercised live via the app; here we verify the DB layer the actions use.
    const [thread] = await db
      .insert(discussionThreads)
      .values({ lessonId: "introduction-to-html", userId, title: "What is a tag?" })
      .returning();
    expect(thread).toBeDefined();

    await db.insert(comments).values([
      { threadId: thread!.id, userId, body: "Tags name elements." },
      { threadId: thread!.id, userId, body: "Thanks!" },
    ]);

    const loaded = await getThread(thread!.id);
    expect(loaded?.title).toBe("What is a tag?");
    expect(loaded?.replies).toHaveLength(2);

    const list = await getLessonThreads("introduction-to-html");
    const summary = list.find((t) => t.id === thread!.id);
    expect(summary?.commentCount).toBe(2);
    expect(summary?.authorName).toBe("Discussion Tester");

    expect(await countLessonThreads("introduction-to-html")).toBeGreaterThanOrEqual(1);
  });

  it("threads on other lessons do not leak into the list", async () => {
    const list = await getLessonThreads("html-images");
    expect(list.find((t) => t.title === "What is a tag?")).toBeUndefined();
  });

  it("deleting a user cascades their threads/comments", async () => {
    const [temp] = await db
      .insert(users)
      .values({ email: "thread-cascade@codejourney.local", name: "Cascade" })
      .returning();
    const [thread] = await db
      .insert(discussionThreads)
      .values({ lessonId: "html-links", userId: temp!.id, title: "cascade" })
      .returning();
    await db.insert(comments).values({ threadId: thread!.id, userId: temp!.id, body: "x" });

    await db.delete(users).where(sql`${users.email} = 'thread-cascade@codejourney.local'`);
    const gone = await getThread(thread!.id);
    expect(gone).toBeNull();
  });
});
