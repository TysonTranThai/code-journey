import { describe, expect, it } from "vitest";

import { getDictionary } from "@/lib/i18n/dictionaries";
import { frameHint, refuseIfSolution } from "@/lib/mentor/guardrails";
import { getErrorExplanation } from "@/lib/mentor/error-explainer";
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

  it("frames hints in Vietnamese when locale is vi", () => {
    expect(frameHint(1, "suy nghĩ về ngữ nghĩa", "vi")).toMatch(/^Gợi ý:/);
    expect(frameHint(2, "xem lại thuộc tính href", "vi")).toMatch(/^Gần đúng rồi:/);
    expect(frameHint(3, "chỉ còn một thẻ nữa", "vi")).toMatch(/^Sắp xong rồi:/);
  });

  it("refuses complete solutions with Vietnamese message when locale is vi", () => {
    const result = refuseIfSolution("Here is the complete solution: <h1>x</h1>", "vi");
    expect(result.refused).toBe(true);
    expect(result.text).toContain("Đó sẽ là toàn bộ lời giải");
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

  it("generates hints in Vietnamese when context locale is vi", async () => {
    const viContext = {
      ...CONTEXT,
      testHints: ["Mỗi dòng cần \\n của riêng nó."],
      locale: "vi",
    };
    const hint2 = await nullMentor.hint(viContext, 2);
    expect(hint2.text).toContain("Hãy tập trung vào yêu cầu này: Mỗi dòng cần \\n của riêng nó.");
    expect(hint2.text).toContain("thẻ hoặc thuộc tính nào cần điều chỉnh?");

    const hint3 = await nullMentor.hint(viContext, 3);
    expect(hint3.text).toContain("Bạn rất gần đích rồi");
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

  it("explains errors in Vietnamese when context locale is vi", async () => {
    const viContext = { ...CONTEXT, locale: "vi" };
    const response = await nullMentor.explainError(
      viContext,
      "dùng thẻ <h1>",
      "Không tìm thấy <h1>",
    );
    expect(response.text).toContain('Bài kiểm tra bị trượt "dùng thẻ <h1>"');
    expect(response.text).toContain("Thông báo lỗi chính là gợi ý đắt giá nhất");
    expect(refuseIfSolution(response.text, "vi").refused).toBe(false);
  });
});

describe("content-as-data sanity", () => {
  it("achievement definitions remain valid (loaded during mentor tests too)", () => {
    expect(getAchievementDefs().length).toBeGreaterThanOrEqual(5);
  });

  it("loads Vietnamese achievement definitions with valid titles and descriptions", () => {
    const viDefs = getAchievementDefs("vi");
    expect(viDefs.length).toBeGreaterThanOrEqual(5);
    const first = viDefs.find((d) => d.id === "first-lesson");
    expect(first?.title).toBe("Những bước đầu tiên");
    expect(first?.description).toBe("Hoàn thành bài học đầu tiên của bạn.");
  });
});

describe("getErrorExplanation (bilingual error explainer and Socratic hints)", () => {
  const dVi = getDictionary("vi");
  const dEn = getDictionary("en");

  it("explains C/C++ '#include' private field error in Vietnamese", () => {
    const raw = "Error: Private field '#include' must be declared in an enclosing class";
    const exp = getErrorExplanation(raw, dVi);
    expect(exp).not.toBeNull();
    expect(exp?.message).toContain("#include");
    expect(exp?.message).toContain("C/C++");
    expect(exp?.hint).toContain("Nộp bài");
  });

  it("explains C/C++ '#include' private field error in English", () => {
    const raw = "Error: Private field '#include' must be declared in an enclosing class";
    const exp = getErrorExplanation(raw, dEn);
    expect(exp).not.toBeNull();
    expect(exp?.message).toContain("#include");
    expect(exp?.message).toContain("C/C++");
    expect(exp?.hint).toContain("Submit");
  });

  it("explains combined '#include' and timeout output properly", () => {
    const raw =
      "Error: Private field '#include' must be declared in an enclosing class\nĐã dừng: mã của bạn chạy quá 2.5s (kiểm tra vòng lặp vô hạn).";
    const exp = getErrorExplanation(raw, dVi);
    expect(exp).not.toBeNull();
    expect(exp?.message).toContain("#include");
    expect(exp?.hint).toContain("Nộp bài");
  });

  it("explains infinite loop timeout error in Vietnamese", () => {
    const raw = "Đã dừng: mã của bạn chạy quá 2.5s (kiểm tra vòng lặp vô hạn).";
    const exp = getErrorExplanation(raw, dVi);
    expect(exp).not.toBeNull();
    expect(exp?.message).toContain("Quá thời gian thực thi");
    expect(exp?.hint).toContain("vòng lặp");
  });

  it("explains infinite loop timeout error in English", () => {
    const raw = "Stopped: your code ran longer than 2.5s (check for infinite loops).";
    const exp = getErrorExplanation(raw, dEn);
    expect(exp).not.toBeNull();
    expect(exp?.message).toContain("Execution Timeout");
    expect(exp?.hint).toContain("loop");
  });

  it("explains syntax errors and reference errors", () => {
    const syntaxExp = getErrorExplanation("SyntaxError: Unexpected token '}'", dVi);
    expect(syntaxExp?.message).toContain("Lỗi cú pháp");

    const refExp = getErrorExplanation("ReferenceError: foo is not defined", dVi);
    expect(refExp?.message).toContain("Lỗi tham chiếu");
  });

  it("explains C language syntax errors through language prop", () => {
    const exp = getErrorExplanation("SyntaxError: Unexpected identifier 'main'", dVi, "c");
    expect(exp?.message).toContain("C/C++");
  });

  it("explains CSP unsafe-eval restriction in Vietnamese and English", () => {
    const raw =
      "Error: Evaluating a string as JavaScript violates the following Content Security Policy directive because 'unsafe-eval' is not an allowed source of script: script-src 'self' 'unsafe-inline'.";
    const expVi = getErrorExplanation(raw, dVi);
    expect(expVi).not.toBeNull();
    expect(expVi?.message).toContain("CSP");
    expect(expVi?.hint).toContain("Nộp bài");

    const expEn = getErrorExplanation(raw, dEn);
    expect(expEn).not.toBeNull();
    expect(expEn?.message).toContain("Content Security Policy");
    expect(expEn?.hint).toContain("Submit");
  });
});
