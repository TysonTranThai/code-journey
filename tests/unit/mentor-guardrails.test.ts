import { describe, expect, it } from "vitest";

import { frameHint, refuseIfSolution } from "@/lib/mentor/guardrails";
import { nullMentor } from "@/lib/mentor/null-mentor";
import type { HintLevel } from "@/lib/mentor/types";
import { getAchievementDefs } from "@/lib/progress/achievement-defs";

const CONTEXT = {
  challengeId: "fix-the-heading",
  challengeTitle: "Fix the Broken Heading",
  prompt: "Change the wrong tag to the correct heading tag.",
  testHints: ["The most important heading on a page is <h1>. Replace <p> with <h1>."],
};

describe("mentor guardrails: refusal filter (ROADMAP Phase 5 criterion 2)", () => {
  it("refuses complete HTML documents", () => {
    const result = refuseIfSolution(
      "<!doctype html><html><body><h1>My First Page</h1></body></html>",
    );
    expect(result.refused).toBe(true);
  });

  it("refuses full <html>…</html> blocks without doctype", () => {
    const result = refuseIfSolution("<html>\n  <h1>My First Page</h1>\n</html>");
    expect(result.refused).toBe(true);
  });

  it("refuses 'here is the complete solution' framings", () => {
    expect(refuseIfSolution("Here is the complete solution: <h1>x</h1>").refused).toBe(true);
    expect(refuseIfSolution("The full answer is: replace everything with this").refused).toBe(true);
    expect(
      refuseIfSolution("Copy and paste this into the editor:\n<h1>My First Page</h1>").refused,
    ).toBe(true);
  });

  it("refuses long fenced code dumps", () => {
    const longCode = "```\n" + "<h1>My First Page</h1>\n".repeat(25) + "```";
    expect(refuseIfSolution(longCode).refused).toBe(true);
  });

  it("allows legitimate educational hints", () => {
    const hints = [
      "The most important heading on a page is <h1>.",
      "Check the closing tag — it needs a slash.",
      "The href value must be quoted.",
      "Nudge: which element wraps the page's main title?",
    ];
    for (const hint of hints) {
      expect(refuseIfSolution(hint).refused).toBe(false);
    }
  });
});

describe("mentor guardrails: hint ladder", () => {
  it("frames hints at ascending levels", () => {
    expect(frameHint(1, "think about semantics")).toMatch(/^Nudge:/);
    expect(frameHint(2, "look at the href")).toMatch(/^Closer:/);
    expect(frameHint(3, "you're one tag away")).toMatch(/^Almost there:/);
  });
});

describe("NullMentor (AI-04 degradation)", () => {
  it("graduates hints by level without emitting full solutions", async () => {
    const levels: HintLevel[] = [1, 2, 3];
    const responses = await Promise.all(levels.map((level) => nullMentor.hint(CONTEXT, level)));
    for (const response of responses) {
      expect(response.text.length).toBeGreaterThan(0);
      expect(refuseIfSolution(response.text).refused).toBe(false);
      // Never a complete heading element (the challenge's answer).
      expect(response.text).not.toMatch(/<h1\s*>[\s\S]*<\/h1>/);
    }
  });

  it("explains errors using the failing test context", async () => {
    const response = await nullMentor.explainError(
      CONTEXT,
      "uses an <h1> element",
      "No <h1> found — the most important heading on a page uses the level-1 heading tag.",
    );
    expect(response.text).toContain("uses an <h1> element");
    expect(refuseIfSolution(response.text).refused).toBe(false);
  });
});

describe("content-as-data sanity", () => {
  it("achievement definitions remain valid (loaded during mentor tests too)", () => {
    expect(getAchievementDefs().length).toBeGreaterThanOrEqual(5);
  });
});
