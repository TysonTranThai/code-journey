import type { HintLevel, MentorAdapter, MentorContext, MentorResponse } from "./types";

/**
 * NullMentor (AI-04): the no-key adapter. It still provides REAL value by
 * composing graduated hints from the challenge's own educational test hints
 * (content-as-data) — no fabricated API, no complete solutions, platform
 * fully functional.
 */
export const nullMentor: MentorAdapter = {
  async hint(context: MentorContext, level: HintLevel): Promise<MentorResponse> {
    const hints = context.testHints.filter((hint) => hint.length > 0);
    const first = hints[0] ?? "Re-read the challenge requirements one line at a time.";

    if (level === 1) {
      return {
        text: `Let's think it through. ${context.challengeTitle} asks you to change the markup so every requirement passes. Start by identifying which element the first requirement talks about, then check what your code currently outputs. (Hint 2 will point closer.)`,
      };
    }
    if (level === 2) {
      return {
        text: `Focus on this requirement: ${first} Compare it with what a correct version would look like — which tag or attribute is involved?`,
      };
    }
    return {
      text: `You're close. The requirement to satisfy: ${first} Write just that one change, run the tests again, and see which requirement (if any) still complains.`,
    };
  },

  async explainError(
    context: MentorContext,
    failedTestName: string,
    errorOutput: string,
  ): Promise<MentorResponse> {
    const relevant =
      context.testHints.find(
        (hint) => failedTestName && failedTestName.length > 0 && hint.length > 0,
      ) ??
      context.testHints[0] ??
      "";
    return {
      text: [
        `The failing test "${failedTestName}" checks one specific requirement.`,
        errorOutput.trim().length > 0
          ? `The error message is your best clue: "${errorOutput.trim().slice(0, 200)}". Errors tell you what the test expected versus what it found.`
          : "Compare what the test expected against what your code produces.",
        relevant ? `Remember: ${relevant}` : "",
        "Fix that one requirement, run again, and read the next message if another test complains.",
      ]
        .filter(Boolean)
        .join(" "),
    };
  },
};
