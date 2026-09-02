import "server-only";

import { and, asc, eq, inArray, lt, or, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import {
  executionJobs,
  submissions,
  type NewExecutionJob,
  type StoredVerdict,
} from "@/lib/db/schema";
import type { JobPayload } from "@/lib/execution/types";

/**
 * Postgres-backed execution queue (03-CONTEXT D-03).
 *
 * Workers claim jobs with SELECT … FOR UPDATE SKIP LOCKED inside a
 * transaction — safe with multiple concurrent runner processes, no extra
 * queue infrastructure. The web tier may enqueue and read; only the runner
 * worker transitions claim/running and writes verdicts.
 */

/** Crash-recovery attempts (requeueStale) before a job is failed. */
export const MAX_ATTEMPTS = 3;
/** Jobs claimed/running longer than this are presumed crashed and requeued. */
export const STALE_THRESHOLD_MS = 2 * 60 * 1000;

export async function enqueueExecution(
  payload: JobPayload,
  submissionId: string | null,
): Promise<string> {
  const [job] = await db
    .insert(executionJobs)
    .values({ payload, submissionId, status: "queued" })
    .returning({ id: executionJobs.id });
  if (!job) throw new Error("enqueueExecution: insert returned no row");
  return job.id;
}

export async function getJob(jobId: string) {
  const [job] = await db.select().from(executionJobs).where(eq(executionJobs.id, jobId)).limit(1);
  return job ?? null;
}

/**
 * Claim the oldest queued job for `workerId`. SKIP LOCKED means two workers
 * racing over the same rows never grab the same job — the loser skips past
 * it. Returns null when the queue is empty.
 */
export async function claimJob(workerId: string): Promise<{
  id: string;
  payload: JobPayload;
  submissionId: string | null;
} | null> {
  return db.transaction(async (tx) => {
    // Raw SQL: drizzle's query builder has no FOR UPDATE SKIP LOCKED combinator.
    const result = await tx.execute<Record<string, unknown>>(
      `SELECT id, payload, submission_id
         FROM execution_jobs
        WHERE status = 'queued'
        ORDER BY created_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED`,
    );
    // postgres-js returns a RowList (array-like) — no `.rows` wrapper.
    const row = result[0] as
      { id: string; payload: JobPayload; submission_id: string | null } | undefined;
    if (!row) return null;

    await tx
      .update(executionJobs)
      .set({
        status: "claimed",
        claimedBy: workerId,
        claimedAt: new Date(),
        attempts: sql`${executionJobs.attempts} + 1`,
      })
      .where(eq(executionJobs.id, row.id));

    return { id: row.id, payload: row.payload, submissionId: row.submission_id };
  });
}

export async function markRunning(jobId: string): Promise<void> {
  await db
    .update(executionJobs)
    .set({ status: "running", startedAt: new Date() })
    .where(eq(executionJobs.id, jobId));
}

/** Write the final verdict and mirror it onto the submission (if any). */
export async function completeJob(jobId: string, verdict: StoredVerdict): Promise<void> {
  const job = await getJob(jobId);
  if (!job) throw new Error(`completeJob: job ${jobId} not found`);

  await db
    .update(executionJobs)
    .set({
      status: "completed",
      verdictPayload: verdict,
      hasVerdict: true,
      finishedAt: new Date(),
      error: null,
    })
    .where(eq(executionJobs.id, jobId));

  if (job.submissionId) {
    const [submission] = await db
      .select({
        id: submissions.id,
        userId: submissions.userId,
        challengeId: submissions.challengeId,
      })
      .from(submissions)
      .where(eq(submissions.id, job.submissionId))
      .limit(1);

    await db
      .update(submissions)
      .set({
        verdict: verdict.verdict,
        perTestResults: verdict.perTestResults,
        runtimeMs: verdict.runtimeMs,
      })
      .where(eq(submissions.id, job.submissionId));

    // Progress hook (Phase 4, PROG-02): a PASSED verdict on an attributed
    // submission is a server-verified challenge completion. Anonymous runs
    // (userId null) never record progress. Best-effort: an award failure
    // must not fail the verdict write (04-CONTEXT D-08).
    if (submission?.userId && verdict.verdict === "passed" && submission.challengeId) {
      try {
        const { recordChallengeCompletion } = await import("@/lib/progress/recording");
        await recordChallengeCompletion(submission.userId, submission.challengeId);
      } catch (err) {
        console.error(
          "[queue] progress recording failed:",
          err instanceof Error ? err.message : err,
        );
      }
    }
  }
}

export async function failJob(jobId: string, error: string): Promise<void> {
  await db
    .update(executionJobs)
    .set({ status: "failed", error, finishedAt: new Date() })
    .where(eq(executionJobs.id, jobId));
}

/**
 * Crash recovery: requeue jobs that were claimed/running but whose worker
 * died (claimedAt older than STALE_THRESHOLD_MS, or never set). Jobs that
 * already burned through MAX_ATTEMPTS are failed instead. Returns the number
 * of jobs requeued.
 */
export async function requeueStale(): Promise<number> {
  const cutoff = new Date(Date.now() - STALE_THRESHOLD_MS);
  const stale = await db
    .select({ id: executionJobs.id, attempts: executionJobs.attempts })
    .from(executionJobs)
    .where(
      and(
        inArray(executionJobs.status, ["claimed", "running"]),
        or(lt(executionJobs.claimedAt, cutoff), sql`${executionJobs.claimedAt} IS NULL`),
      ),
    );

  let requeued = 0;
  for (const job of stale) {
    if (job.attempts >= MAX_ATTEMPTS) {
      await failJob(job.id, "max attempts exceeded (stale worker)");
    } else {
      await db
        .update(executionJobs)
        .set({ status: "queued", claimedBy: null, claimedAt: null })
        .where(eq(executionJobs.id, job.id));
      requeued += 1;
    }
  }
  return requeued;
}

/** Latest job for a submission (used by the verdict polling endpoint). */
export async function getLatestJobForSubmission(submissionId: string) {
  const [job] = await db
    .select()
    .from(executionJobs)
    .where(eq(executionJobs.submissionId, submissionId))
    .orderBy(asc(executionJobs.createdAt))
    .limit(1);
  return job ?? null;
}

export type { NewExecutionJob };
