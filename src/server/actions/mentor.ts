"use server";

import { requireUser } from "@/lib/auth/guards";
import { nullMentor } from "@/lib/mentor/null-mentor";
import { frameHint, refuseIfSolution } from "@/lib/mentor/guardrails";
import { checkMentorQuota, recordMentorRequest, type MentorKind } from "@/lib/mentor/rate-limit";
import type { HintLevel, MentorContext } from "@/lib/mentor/types";

/**
 * Mentor server actions (AI-01…04). Server-side enforcement order:
 * 1. requireUser — anonymous users cannot invoke the mentor (also PLAT-08)
 * 2. quota — friendly per-user daily limits (AI-03)
 * 3. adapter — NullMentor until a real provider key exists (AI-04)
 * 4. refusal filter — solution-like responses never reach the client
 */

export interface MentorActionResult {
  ok: true;
  text: string;
  refused: boolean;
  remaining: number;
}

export interface MentorActionError {
  ok: false;
  error: string;
}

/** Resolve the current adapter: env-gated; NullMentor is the v1 default. */
async function getAdapter() {
  // A real provider adapter lands here when MENTOR_API_KEY + a provider
  // choice exist. Until then the seam keeps the platform fully functional.
  return nullMentor;
}

export async function requestHint(
  context: MentorContext,
  level: HintLevel,
): Promise<MentorActionResult | MentorActionError> {
  const session = await requireUser();
  const userId = session.user.id;
  const kind: MentorKind = "hintsPerDay";

  const quota = await checkMentorQuota(userId, kind);
  if (!quota.allowed) {
    return {
      ok: false,
      error: "You've used all your hints for today. Come back tomorrow — the challenge will keep.",
    };
  }

  const adapter = await getAdapter();
  const raw = await adapter.hint(context, level);
  const filtered = refuseIfSolution(raw.text);
  await recordMentorRequest(userId, kind);

  const framed = frameHint(level, filtered.text);
  return {
    ok: true,
    text: framed,
    refused: filtered.refused,
    remaining: quota.remaining - 1,
  };
}

export async function explainError(
  context: MentorContext,
  failedTestName: string,
  errorOutput: string,
): Promise<MentorActionResult | MentorActionError> {
  const session = await requireUser();
  const userId = session.user.id;
  const kind: MentorKind = "explainsPerDay";

  const quota = await checkMentorQuota(userId, kind);
  if (!quota.allowed) {
    return {
      ok: false,
      error: "You've reached today's error-explanation limit. Try again tomorrow.",
    };
  }

  const adapter = await getAdapter();
  const raw = await adapter.explainError(context, failedTestName, errorOutput);
  const filtered = refuseIfSolution(raw.text);
  await recordMentorRequest(userId, kind);

  return {
    ok: true,
    text: filtered.text,
    refused: filtered.refused,
    remaining: quota.remaining - 1,
  };
}
