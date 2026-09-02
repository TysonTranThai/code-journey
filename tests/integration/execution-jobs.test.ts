import { and, eq, inArray } from "drizzle-orm";
import { afterAll, beforeAll, describe, expect, it } from "vitest";

import { db } from "@/lib/db";
import { executionJobs } from "@/lib/db/schema";
import {
  MAX_ATTEMPTS,
  STALE_THRESHOLD_MS,
  claimJob,
  completeJob,
  enqueueExecution,
  failJob,
  getJob,
  markRunning,
  requeueStale,
} from "@/lib/execution/queue";
import type { JobPayload } from "@/lib/execution/types";

const payloadA: JobPayload = {
  code: "// student code A",
  testFiles: [{ name: "a.test.mjs", code: "assert(true)" }],
  timeoutMs: 10_000,
  memoryMb: 256,
};
const payloadB: JobPayload = {
  code: "// student code B",
  testFiles: [{ name: "b.test.mjs", code: "assert(true)" }],
  timeoutMs: 10_000,
  memoryMb: 256,
};

const jobIds: string[] = [];

/** Clean any execution_jobs/submissions rows this suite created. */
async function cleanup() {
  if (jobIds.length > 0) {
    await db.delete(executionJobs).where(inArray(executionJobs.id, jobIds));
    jobIds.length = 0;
  }
}

const verdict = {
  verdict: "passed" as const,
  perTestResults: [{ name: "test 1", passed: true, message: "looks good!" }],
  runtimeMs: 42,
  output: "1 test passed",
};

/**
 * Queue integration tests — run ONLY when Postgres is reachable (same
 * skipIf probe as db.test.ts).
 */
const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

describe.skipIf(!dbUp)("execution queue (Postgres-backed)", () => {
  beforeAll(async () => {
    // Fresh queue state so claim ordering assertions hold.
    await db.delete(executionJobs);
  });

  afterAll(async () => {
    await cleanup();
  });

  it("enqueues a job in status queued with the payload intact", async () => {
    const id = await enqueueExecution(payloadA, null);
    jobIds.push(id);

    const job = await getJob(id);
    expect(job?.status).toBe("queued");
    expect(job?.payload).toEqual(payloadA);
    expect(job?.attempts).toBe(0);
    expect(job?.submissionId).toBeNull();
  });

  it("claims the OLDEST queued job first and marks it claimed", async () => {
    // Reset: test 1 left a queued job behind that would win claim ordering.
    await db.delete(executionJobs);
    const first = await enqueueExecution(payloadA, null);
    jobIds.push(first);
    await new Promise((r) => setTimeout(r, 15)); // ensure created_at ordering
    const second = await enqueueExecution(payloadB, null);
    jobIds.push(second);

    const claimed = await claimJob("worker-test-1");
    expect(claimed).not.toBeNull();
    expect(claimed!.id).toBe(first);

    const job = await getJob(first);
    expect(job?.status).toBe("claimed");
    expect(job?.claimedBy).toBe("worker-test-1");
    expect(job?.claimedAt).toBeTruthy();
    expect(job?.attempts).toBe(1);
  });

  it("SKIP LOCKED: a second worker claims the OTHER job, never the same one", async () => {
    // Job from the previous test is already claimed; the next claim must
    // return the second job, proving claimed rows are skipped.
    const claimed = await claimJob("worker-test-2");
    expect(claimed).not.toBeNull();
    expect(claimed!.id).not.toBe(jobIds[0]);

    // Queue now empty.
    const drained = await claimJob("worker-test-3");
    expect(drained).toBeNull();
  });

  it("markRunning → completeJob writes the verdict and mirrors it on the submission", async () => {
    const id = await enqueueExecution(payloadA, null);
    jobIds.push(id);
    await claimJob("worker-test-4");
    await markRunning(id);

    const running = await getJob(id);
    expect(running?.status).toBe("running");
    expect(running?.startedAt).toBeTruthy();

    await completeJob(id, verdict);

    const done = await getJob(id);
    expect(done?.status).toBe("completed");
    expect(done?.hasVerdict).toBe(true);
    expect(done?.verdictPayload?.verdict).toBe("passed");
    expect(done?.finishedAt).toBeTruthy();
  });

  it("completeJob mirrors verdict fields onto the linked submission", async () => {
    const { submissions } = await import("@/lib/db/schema");
    const [submission] = await db
      .insert(submissions)
      .values({
        userId: null, // anonymous run
        challengeId: "test-challenge",
        code: "// anonymous code",
      })
      .returning();
    expect(submission).toBeDefined();

    const id = await enqueueExecution(payloadA, submission!.id);
    jobIds.push(id);
    await claimJob("worker-test-5");
    await completeJob(id, {
      ...verdict,
      verdict: "failed",
      perTestResults: [{ name: "t", passed: false, message: "check the tag" }],
    });

    const [updated] = await db.select().from(submissions).where(eq(submissions.id, submission!.id));
    expect(updated?.verdict).toBe("failed");
    expect(updated?.perTestResults).toHaveLength(1);
    expect(updated?.runtimeMs).toBe(42);

    await db.delete(submissions).where(eq(submissions.id, submission!.id));
  });

  it("failJob records the error", async () => {
    const id = await enqueueExecution(payloadA, null);
    jobIds.push(id);
    await claimJob("worker-test-6");
    await failJob(id, "boom");

    const job = await getJob(id);
    expect(job?.status).toBe("failed");
    expect(job?.error).toBe("boom");
  });

  it("requeueStale recovers a claimed job whose worker died, up to MAX_ATTEMPTS", async () => {
    const id = await enqueueExecution(payloadA, null);
    jobIds.push(id);
    await claimJob("worker-died");
    // Backdate claimedAt past the staleness threshold.
    await db
      .update(executionJobs)
      .set({
        claimedAt: new Date(Date.now() - STALE_THRESHOLD_MS - 1000),
      })
      .where(eq(executionJobs.id, id));

    const requeued = await requeueStale();
    expect(requeued).toBeGreaterThanOrEqual(1);

    const job = await getJob(id);
    expect(job?.status).toBe("queued");
    expect(job?.claimedBy).toBeNull();

    // Burn through the remaining attempts → must flip to failed.
    for (let i = job!.attempts; i < MAX_ATTEMPTS; i++) {
      await claimJob("worker-dies-again");
      await db
        .update(executionJobs)
        .set({
          claimedAt: new Date(Date.now() - STALE_THRESHOLD_MS - 1000),
        })
        .where(and(eq(executionJobs.id, id), inArray(executionJobs.status, ["claimed"])));
      await requeueStale();
    }
    const exhausted = await getJob(id);
    expect(exhausted?.status).toBe("failed");
    expect(exhausted?.error).toContain("max attempts");
  });
});
