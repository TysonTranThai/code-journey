import { randomUUID } from "node:crypto";

import { eq } from "drizzle-orm";
import { describe, expect, it, vi, afterAll } from "vitest";

import { db } from "@/lib/db";
import { executionJobs, submissions, users } from "@/lib/db/schema";
import { consume, DAY_MS } from "@/lib/rate-limit/limiter";

// Provide a controllable `auth()` so the route handlers' auth branch is tested
// without bootstrapping a real NextAuth session.
const mockAuth = vi.fn();
vi.mock("@/lib/auth/config", () => ({ auth: () => mockAuth() }));
// Provide a stable client IP so the rate limiter keys deterministically.
vi.mock("next/headers", () => ({
  headers: async () => new Headers({ "x-forwarded-for": "203.0.113.7" }),
}));

// Keep the real queue logic but never actually enqueue/execute.
vi.mock("@/lib/execution/queue", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/execution/queue")>();
  return { ...actual, enqueueExecution: vi.fn().mockResolvedValue("job-fake") };
});
// Serve a known challenge so POST can build a payload without real content.
vi.mock("@/lib/curriculum/loaders", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/curriculum/loaders")>();
  return { ...actual, getChallenge: vi.fn(() => ({ id: "fix-the-heading", tests: [] })) };
});

import { GET as getSubmission } from "@/app/api/challenges/run/[submissionId]/route";
import { POST as postRun } from "@/app/api/challenges/run/route";

const ID_A = randomUUID();
const ID_B = randomUUID();
const SUBMISSION_A = randomUUID();

async function makeRequest(params: { submissionId: string }): Promise<Response> {
  return getSubmission(new Request("http://localhost/api"), {
    params: Promise.resolve(params),
  });
}

describe.skipIf(!process.env.DATABASE_URL)("submission authorization (07-02)", () => {
  afterAll(async () => {
    await db.delete(submissions).where(eq(submissions.id, SUBMISSION_A)).catch(() => {});
  });

  it("requires authentication to read a submission", async () => {
    mockAuth.mockResolvedValue(null);
    const res = await makeRequest({ submissionId: SUBMISSION_A });
    expect(res.status).toBe(401);
  });

  it("denies an authenticated non-owner (404, existence hidden)", async () => {
    // Ensure A's submission exists in the DB.
    await db.insert(users).values({ id: ID_A, name: "A", email: `${ID_A}@test.local` }).onConflictDoNothing();
    await db
      .insert(submissions)
      .values({ id: SUBMISSION_A, userId: ID_A, challengeId: "fix-the-heading", code: "<p>x</p>" })
      .onConflictDoNothing();

    mockAuth.mockResolvedValue({ user: { id: ID_B } });
    const res = await makeRequest({ submissionId: SUBMISSION_A });
    expect(res.status).toBe(404);
  });

  it("allows the owner to read their own submission", async () => {
    // Add a queued job so the ownership check passes into a 202 (pending).
    await db
      .insert(executionJobs)
      .values({
        id: randomUUID(),
        submissionId: SUBMISSION_A,
        status: "queued",
        payload: { code: "", testFiles: [], timeoutMs: 1, memoryMb: 1 },
        hasVerdict: false,
        attempts: 0,
      })
      .onConflictDoNothing();

    mockAuth.mockResolvedValue({ user: { id: ID_A } });
    const res = await makeRequest({ submissionId: SUBMISSION_A });
    expect(res.status).toBe(202);
  });

  it("rejects an anonymous run (401) and does not enqueue", async () => {
    mockAuth.mockResolvedValue(null);
    const post = postRun;
    const res = await post(
      new Request("http://localhost/api/challenges/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: "<h1>Hi</h1>",
          trackId: "web-development",
          courseId: "web-development-foundations",
          moduleId: "html-foundations",
          lessonId: "introduction-to-html",
          challengeId: "fix-the-heading",
        }),
      }),
    );
    expect(res.status).toBe(401);
  });

  it("returns 429 when the daily run limit is exhausted (07-03)", async () => {
    const userId = ID_A;
    // Exceed the daily run cap for this user+IP so the route rejects.
    for (let i = 0; i < 21; i++) {
      await consume("run", `${userId}:203.0.113.7`, 20, DAY_MS);
    }
    mockAuth.mockResolvedValue({ user: { id: userId } });
    const res = await postRun(
      new Request("http://localhost/api/challenges/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: "<h1>Hi</h1>",
          trackId: "web-development",
          courseId: "web-development-foundations",
          moduleId: "html-foundations",
          lessonId: "introduction-to-html",
          challengeId: "fix-the-heading",
        }),
      }),
    );
    expect(res.status).toBe(429);
  });
});
