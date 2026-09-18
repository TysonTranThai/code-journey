import { NextResponse } from "next/server";
import { z } from "zod";

import { auth } from "@/lib/auth/config";
import { enqueueExecution } from "@/lib/execution/queue";
import type { JobPayload } from "@/lib/execution/types";
import { getChallenge, getPracticeChallenge } from "@/lib/curriculum/loaders";
import { getServerI18n } from "@/lib/i18n/server";
import { clientIp, consume, DAY_MS, MINUTE_MS } from "@/lib/rate-limit/limiter";

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
  /** Required for lesson-attached challenges (checkpoints). */
  lessonId: z.string().min(1).optional(),
  /** Required for practice-set challenges. */
  practiceId: z.string().min(1).optional(),
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
  const { code, trackId, courseId, moduleId, lessonId, practiceId, challengeId } = parsed.data;

  // Challenge must exist in version-controlled content — client-supplied
  // tests are never trusted. Practice challenges resolve through their set;
  // lesson challenges (checkpoints) through the lesson.
  const { locale } = await getServerI18n();
  let challenge;
  try {
    if (practiceId) {
      challenge = getPracticeChallenge(trackId, courseId, moduleId, practiceId, challengeId, undefined, locale);
    } else if (lessonId) {
      challenge = getChallenge(trackId, courseId, moduleId, lessonId, challengeId, undefined, locale);
    } else {
      return NextResponse.json(
        { error: "invalid body", issues: ["lessonId or practiceId is required"] },
        { status: 400 },
      );
    }
  } catch {
    return NextResponse.json({ error: "challenge not found" }, { status: 404 });
  }

  const payload: JobPayload = {
    code,
    // Server-side test definitions only.
    testFiles: challenge.tests.map((t) => ({ name: t.name, code: t.code })),
    // Java needs the largest budget: a fresh javac + JVM per test. C, C++,
    // and C# compile per test but are fast (~0.04–0.5 s per unit, probed).
    timeoutMs:
      challenge.language === "java"
        ? 40_000
        : challenge.language === "cpp" || challenge.language === "c" || challenge.language === "csharp"
          ? 20_000
          : 10_000,
    memoryMb:
      challenge.language === "cpp" || challenge.language === "java" || challenge.language === "c" || challenge.language === "csharp"
        ? 512
        : 256,
    // Python, C++, Java, C, and C# tracks: route the job to the matching runtime branch.
    language:
      challenge.language === "python"
        ? "python"
        : challenge.language === "cpp"
          ? "cpp"
          : challenge.language === "java"
            ? "java"
            : challenge.language === "c"
              ? "c"
              : challenge.language === "csharp"
                ? "csharp"
                : "javascript",
  };

  const session = await auth();
  if (!session?.user?.id) {
    // DECIDED (07-02): code execution requires an authenticated account.
    return NextResponse.json({ error: "authentication required" }, { status: 401 });
  }

  // Rate limit (07-03): each run spawns an isolated execution workload, so
  // limit per user+IP with a daily cap and a short per-minute burst. Sized
  // for auto-check (the workspace re-submits while the learner types), with
  // the burst high enough that normal typing pauses never hit 429.
  const ip = await clientIp();
  const daily = await consume("run", `${session.user.id}:${ip}`, 400, DAY_MS);
  if (!daily.allowed) {
    return NextResponse.json(
      { error: (await getServerI18n()).d.errors.dailyLimit },
      { status: 429 },
    );
  }
  const burst = await consume("run-burst", `${session.user.id}:${ip}`, 12, MINUTE_MS);
  if (!burst.allowed) {
    return NextResponse.json(
      { error: (await getServerI18n()).d.errors.burstLimit },
      { status: 429 },
    );
  }

  const db = (await import("@/lib/db")).db;
  const { submissions } = await import("@/lib/db/schema");

  const [submission] = await db
    .insert(submissions)
    .values({
      userId: session.user.id,
      challengeId,
      code,
    })
    .returning({ id: submissions.id });

  if (!submission) {
    return NextResponse.json({ error: "could not record submission" }, { status: 500 });
  }

  const jobId = await enqueueExecution(payload, submission.id);

  // In development, trigger background execution if no standalone worker claimed it within 300ms.
  // This guarantees local testing never times out even if `pnpm worker` is not running.
  if (process.env.NODE_ENV !== "production") {
    void (async () => {
      try {
        await new Promise((r) => setTimeout(r, 300));
        const { claimJob, completeJob, markRunning } = await import("@/lib/execution/queue");
        const { executeJob } = await import("@/workers/execute");
        const { truncateOutput } = await import("@/lib/execution/types");
        const job = await claimJob("dev-fallback-worker");
        if (job) {
          await markRunning(job.id);
          const verdict = await executeJob(job.payload);
          await completeJob(job.id, {
            ...verdict,
            output: truncateOutput(verdict.output),
          });
        }
      } catch (err) {
        console.error("[dev-fallback-worker] error:", err);
      }
    })();
  }

  return NextResponse.json({ submissionId: submission.id, jobId }, { status: 202 });
}
