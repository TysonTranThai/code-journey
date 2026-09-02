import { NextResponse } from "next/server";
import { z } from "zod";

import { auth } from "@/lib/auth/config";
import { ProgressVerificationError, recordLessonCompletion } from "@/lib/progress/recording";

/**
 * Lesson-completion endpoint (PROG-01/02). Requires an authenticated
 * session; the server verifies the lesson's challenges were passed before
 * recording. Anonymous → 401; unverified → 403; success → 201/200.
 */
const bodySchema = z.object({
  trackId: z.string().min(1),
  courseId: z.string().min(1),
  moduleId: z.string().min(1),
  lessonId: z.string().min(1),
});

export async function POST(request: Request) {
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) {
    return NextResponse.json({ error: "authentication required" }, { status: 401 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "invalid JSON body" }, { status: 400 });
  }

  const parsed = bodySchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: "invalid body" }, { status: 400 });
  }

  try {
    const result = await recordLessonCompletion(
      userId,
      parsed.data.trackId,
      parsed.data.courseId,
      parsed.data.moduleId,
      parsed.data.lessonId,
    );
    return NextResponse.json(result, { status: result.recorded ? 201 : 200 });
  } catch (err) {
    if (err instanceof ProgressVerificationError) {
      return NextResponse.json({ error: err.message }, { status: 403 });
    }
    // Unknown lesson id (CurriculumNotFoundError) or unexpected failure.
    return NextResponse.json({ error: "lesson not found" }, { status: 404 });
  }
}
