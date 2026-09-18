import { NextResponse } from "next/server";
import { z } from "zod";

import { auth } from "@/lib/auth/config";
import { db } from "@/lib/db";
import { progressEvents } from "@/lib/db/schema";
import { and, eq, inArray } from "drizzle-orm";

/**
 * Read-only progress for practice sets (Course 1 revision).
 *
 * Returns which of the requested challenge ids the signed-in user has
 * passed (progress_events, contentType "challenge" — server-written only,
 * on a passed verdict). Read-your-own-records only: no ids of other users
 * are involved, and nothing here can mutate state.
 */
const querySchema = z.object({
  ids: z
    .string()
    .max(2_000)
    .regex(/^[a-z0-9]+(-[a-z0-9]+)*(,[a-z0-9]+(-[a-z0-9]+)*)*$/, "expected comma-separated slugs"),
});

export async function GET(request: Request) {
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) {
    // Anonymous: no personal progress exists; the client shows a neutral state.
    return NextResponse.json({ completed: [] as string[], authenticated: false });
  }

  const url = new URL(request.url);
  const parsed = querySchema.safeParse({ ids: url.searchParams.get("ids") ?? "" });
  if (!parsed.success) {
    return NextResponse.json({ error: "invalid ids" }, { status: 400 });
  }
  const ids = [...new Set(parsed.data.ids.split(","))].slice(0, 100);
  if (ids.length === 0) {
    return NextResponse.json({ completed: [], authenticated: true });
  }

  const rows = await db
    .select({ contentId: progressEvents.contentId })
    .from(progressEvents)
    .where(
      and(
        eq(progressEvents.userId, userId),
        eq(progressEvents.contentType, "challenge"),
        inArray(progressEvents.contentId, ids),
      ),
    );

  return NextResponse.json({
    completed: rows.map((r) => r.contentId),
    authenticated: true,
  });
}
