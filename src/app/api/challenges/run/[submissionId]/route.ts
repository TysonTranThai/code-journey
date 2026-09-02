import { eq } from "drizzle-orm";
import { NextResponse } from "next/server";

import { db } from "@/lib/db";
import { submissions } from "@/lib/db/schema";
import { getLatestJobForSubmission } from "@/lib/execution/queue";

/**
 * Verdict polling endpoint (CHAL-02). The UI polls this after a 202 from
 * POST /api/challenges/run until the job has a verdict.
 *
 * Returns 202 while pending, 200 with the verdict once available.
 */
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ submissionId: string }> },
) {
  const { submissionId } = await params;

  const [submission] = await db
    .select()
    .from(submissions)
    .where(eq(submissions.id, submissionId))
    .limit(1);

  if (!submission) {
    return NextResponse.json({ error: "submission not found" }, { status: 404 });
  }

  const job = await getLatestJobForSubmission(submissionId);
  if (!job) {
    return NextResponse.json({ error: "execution job not found" }, { status: 404 });
  }

  if (!job.hasVerdict || !job.verdictPayload) {
    return NextResponse.json({ status: job.status }, { status: 202 });
  }

  return NextResponse.json({
    status: job.status,
    verdict: job.verdictPayload.verdict,
    perTestResults: job.verdictPayload.perTestResults,
    runtimeMs: job.verdictPayload.runtimeMs,
    output: job.verdictPayload.output,
  });
}
