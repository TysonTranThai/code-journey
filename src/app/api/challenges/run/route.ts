import { NextResponse } from "next/server";
import { z } from "zod";

import { auth } from "@/lib/auth/config";
import { enqueueExecution } from "@/lib/execution/queue";
import type { JobPayload } from "@/lib/execution/types";
import { getChallenge } from "@/lib/curriculum/loaders";

/**
 * Code-run endpoint (CHAL-02, PLAT-08).
 *
 * Validates the submitted code, creates the submission snapshot, enqueues an
 * execution job, and returns ids for polling. NO code executes here — the
 * runner worker (separate process) picks the job up and runs it in the
 * hardened sandbox (03-02).
 *
 * Anonymous users may RUN (rate limiting lands in Phase 6 hardening);
 * logged-in users get their submission attributed (CHAL-03).
 *
 * Response: 202 { submissionId, jobId } — verdict arrives via
 * GET /api/challenges/run/[submissionId].
 */

const bodySchema = z.object({
  code: z.string().min(1).max(50_000),
  trackId: z.string().min(1),
  courseId: z.string().min(1),
  moduleId: z.string().min(1),
  lessonId: z.string().min(1),
  challengeId: z.string().min(1),
});

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "invalid JSON body" }, { status: 400 });
  }

  const parsed = bodySchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "invalid body", issues: parsed.error.issues.map((i) => i.message) },
      { status: 400 },
    );
  }
  const { code, trackId, courseId, moduleId, lessonId, challengeId } = parsed.data;

  // Challenge must exist in version-controlled content — client-supplied
  // tests are never trusted.
  let challenge;
  try {
    challenge = getChallenge(trackId, courseId, moduleId, lessonId, challengeId);
  } catch {
    return NextResponse.json({ error: "challenge not found" }, { status: 404 });
  }

  const payload: JobPayload = {
    code,
    // Server-side test definitions only.
    testFiles: challenge.tests.map((t) => ({ name: t.name, code: t.code })),
    timeoutMs: 10_000,
    memoryMb: 256,
  };

  const session = await auth();
  const db = (await import("@/lib/db")).db;
  const { submissions } = await import("@/lib/db/schema");

  const [submission] = await db
    .insert(submissions)
    .values({
      userId: session?.user?.id ?? null,
      challengeId,
      code,
    })
    .returning({ id: submissions.id });

  if (!submission) {
    return NextResponse.json({ error: "could not record submission" }, { status: 500 });
  }

  const jobId = await enqueueExecution(payload, submission.id);

  return NextResponse.json({ submissionId: submission.id, jobId }, { status: 202 });
}
