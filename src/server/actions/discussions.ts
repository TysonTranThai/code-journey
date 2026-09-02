"use server";

import { eq } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { z } from "zod";

import { db } from "@/lib/db";
import { comments, discussionThreads } from "@/lib/db/schema";
import { requireUser } from "@/lib/auth/guards";

/**
 * Discussion write actions (COMM-01/02). Authentication and validation are
 * enforced SERVER-SIDE: anonymous users are rejected before any DB access,
 * and authorship always derives from the session, never client input.
 */

const createThreadSchema = z.object({
  lessonId: z.string().min(1).max(120),
  title: z.string().trim().min(1).max(200),
  body: z.string().trim().min(1).max(4000),
});

const addReplySchema = z.object({
  threadId: z.string().min(1).max(120),
  body: z.string().trim().min(1).max(4000),
});

export async function createThread(
  lessonId: string,
  title: string,
  body: string,
): Promise<{ ok: true; threadId: string } | { ok: false; error: string }> {
  const session = await requireUser();

  const parsed = createThreadSchema.safeParse({ lessonId, title, body });
  if (!parsed.success) {
    return { ok: false, error: "Title and question are required (max 200 / 4000 chars)." };
  }

  const [thread] = await db
    .insert(discussionThreads)
    .values({
      lessonId: parsed.data.lessonId,
      userId: session.user.id,
      title: parsed.data.title,
    })
    .returning({ id: discussionThreads.id });
  if (!thread) return { ok: false, error: "Could not create the thread." };

  await db.insert(comments).values({
    threadId: thread.id,
    userId: session.user.id,
    body: parsed.data.body,
  });

  revalidatePath(`/learn`);
  return { ok: true, threadId: thread.id };
}

export async function addReply(
  threadId: string,
  body: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  const session = await requireUser();

  const parsed = addReplySchema.safeParse({ threadId, body });
  if (!parsed.success) {
    return { ok: false, error: "Reply is required (max 4000 chars)." };
  }

  const [thread] = await db
    .select({ id: discussionThreads.id })
    .from(discussionThreads)
    .where(eq(discussionThreads.id, parsed.data.threadId))
    .limit(1);
  if (!thread) return { ok: false, error: "Thread not found." };

  await db.insert(comments).values({
    threadId: thread.id,
    userId: session.user.id,
    body: parsed.data.body,
  });

  revalidatePath(`/learn`);
  return { ok: true };
}
