import "server-only";

import { asc, desc, eq, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import { comments, discussionThreads, users } from "@/lib/db/schema";

/**
 * Discussion read layer (COMM-03): public queries — no auth required.
 * Write paths live in server actions only.
 */

export interface ThreadSummary {
  id: string;
  title: string;
  authorName: string | null;
  commentCount: number;
  createdAt: Date;
}

export interface ThreadWithReplies {
  id: string;
  title: string;
  authorName: string | null;
  createdAt: Date;
  replies: {
    id: string;
    body: string;
    authorName: string | null;
    createdAt: Date;
  }[];
}

export async function getLessonThreads(lessonId: string): Promise<ThreadSummary[]> {
  const rows = await db
    .select({
      id: discussionThreads.id,
      title: discussionThreads.title,
      authorName: users.name,
      createdAt: discussionThreads.createdAt,
      commentCount: sql<number>`count(${comments.id})::int`,
    })
    .from(discussionThreads)
    .leftJoin(users, eq(users.id, discussionThreads.userId))
    .leftJoin(comments, eq(comments.threadId, discussionThreads.id))
    .where(eq(discussionThreads.lessonId, lessonId))
    .groupBy(discussionThreads.id, discussionThreads.title, users.name, discussionThreads.createdAt)
    .orderBy(desc(discussionThreads.createdAt));
  return rows;
}

export async function getThread(threadId: string): Promise<ThreadWithReplies | null> {
  const [thread] = await db
    .select({
      id: discussionThreads.id,
      title: discussionThreads.title,
      authorName: users.name,
      createdAt: discussionThreads.createdAt,
    })
    .from(discussionThreads)
    .leftJoin(users, eq(users.id, discussionThreads.userId))
    .where(eq(discussionThreads.id, threadId))
    .limit(1);
  if (!thread) return null;

  const replies = await db
    .select({
      id: comments.id,
      body: comments.body,
      authorName: users.name,
      createdAt: comments.createdAt,
    })
    .from(comments)
    .leftJoin(users, eq(users.id, comments.userId))
    .where(eq(comments.threadId, threadId))
    .orderBy(asc(comments.createdAt));

  return { ...thread, replies };
}

/** The lesson a thread anchors to (used to verify the URL context). */
export async function getThreadLessonId(threadId: string): Promise<string | null> {
  const [thread] = await db
    .select({ lessonId: discussionThreads.lessonId })
    .from(discussionThreads)
    .where(eq(discussionThreads.id, threadId))
    .limit(1);
  return thread?.lessonId ?? null;
}

export async function countLessonThreads(lessonId: string): Promise<number> {
  const [row] = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(discussionThreads)
    .where(eq(discussionThreads.lessonId, lessonId));
  return row?.count ?? 0;
}
