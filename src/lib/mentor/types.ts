/**
 * Mentor adapter seam (05-CONTEXT D-05, PLAT-08).
 *
 * The mentor is a SERVER-SIDE service only — no provider calls from the
 * browser. Provider-agnostic: a real adapter (Anthropic/OpenAI/local) plugs
 * in when a key exists; until then NullMentor serves content-derived help.
 *
 * Pedagogy contract: responses TEACH — graduated hints and error
 * explanations — never complete solutions (guardrails enforce, tests prove).
 */

export interface MentorContext {
  challengeId: string;
  challengeTitle: string;
  prompt: string;
  /** Educational hints from the challenge's own tests (content-as-data). */
  testHints: string[];
  boilerplate?: string;
}

/** 1 = nudge, 2 = direction, 3 = near-miss. Never the final code. */
export type HintLevel = 1 | 2 | 3;

export interface MentorResponse {
  text: string;
  /** True when the guardrail rejected a solution-like response. */
  refused?: boolean;
}

export interface MentorAdapter {
  hint(context: MentorContext, level: HintLevel): Promise<MentorResponse>;
  explainError(
    context: MentorContext,
    failedTestName: string,
    errorOutput: string,
  ): Promise<MentorResponse>;
}

/** True when a real AI provider is configured (AI-04 graceful degradation). */
export function mentorAvailable(): boolean {
  return Boolean(process.env.MENTOR_API_KEY);
}
