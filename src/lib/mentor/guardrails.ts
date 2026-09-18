import type { HintLevel } from "./types";

/**
 * Mentor guardrails (05-CONTEXT D-07): the mentor teaches, never solves.
 * Enforced SERVER-SIDE before any response reaches the client; proven by the
 * adversarial refusal test suite (ROADMAP Phase 5 criterion 2).
 */

const SOLUTION_MARKERS: RegExp[] = [
  // Complete documents or full code dumps
  /<html[\s\S]*<\/html>/i,
  /<!doctype\s+html/i,
  /<body[\s\S]*<\/body>/i,
  // "Here's the solution" framings
  /here('s| is) the (complete |full )?(solution|answer|code)/i,
  /the (complete |full )?(solution|answer) is/i,
  /copy (and|&) paste (this|the following)/i,
  // Whole-code fences around long blocks (hints are prose, not fenced code)
  /```[\s\S]{200,}```/,
];

/**
 * Refuse responses that look like a complete solution. Returns the original
 * text when acceptable, or a refusal response.
 */
export function refuseIfSolution(
  text: string,
  locale?: string,
): { text: string; refused: boolean } {
  for (const marker of SOLUTION_MARKERS) {
    if (marker.test(text)) {
      return {
        refused: true,
        text:
          locale === "vi"
            ? "Đó sẽ là toàn bộ lời giải — chúng ta hãy cùng học từng bước nhé. Hãy mô tả phần bạn đang gặp khó khăn, tôi sẽ hướng dẫn cho bạn."
            : "That would be the whole answer — let's not skip the learning. Try describing which part you're stuck on, and I'll guide you to it.",
      };
    }
  }
  return { text, refused: false };
}

const LEVEL_FRAME_EN: Record<HintLevel, string> = {
  1: "Nudge:",
  2: "Closer:",
  3: "Almost there:",
};

const LEVEL_FRAME_VI: Record<HintLevel, string> = {
  1: "Gợi ý:",
  2: "Gần đúng rồi:",
  3: "Sắp xong rồi:",
};

/** Frame a hint at its ladder level (never rewrites the pedagogy, only tone). */
export function frameHint(level: HintLevel, text: string, locale?: string): string {
  const frameMap = locale === "vi" ? LEVEL_FRAME_VI : LEVEL_FRAME_EN;
  return `${frameMap[level]} ${text}`;
}
