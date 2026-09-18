import { describe, expect, it } from "vitest";

import {
  getModuleFlow,
  getModulePractices,
  getPracticeChallenge,
  getPracticeChallenges,
  getPracticeSet,
} from "@/lib/curriculum/loaders";

const TRACK = "web-development";
const COURSE = "web-development-beginner";

describe("practice set loaders (real content)", () => {
  it("loads every module's practice sets in declared order with location", () => {
    const html = getModulePractices(TRACK, COURSE, "html-foundations");
    expect(html.map((p) => p.id)).toEqual([
      "introduction-to-html-practice",
      "html-structure-practice",
      "html-links-practice",
      "html-images-practice",
      "html-lists-and-tables-practice",
      "html-semantics-practice",
      "html-forms-practice",
      "personal-profile-project-practice",
    ]);
    for (const [i, p] of html.entries()) {
      expect(p.trackId).toBe(TRACK);
      expect(p.courseId).toBe(COURSE);
      expect(p.moduleId).toBe("html-foundations");
      expect(p.practiceIndex).toBe(i);
      expect(p.minutes).toBeGreaterThan(0);
    }
  });

  it("resolves a single practice set and throws for unknown ids", () => {
    const set = getPracticeSet(TRACK, COURSE, "html-foundations", "html-structure-practice");
    expect(set.afterLesson).toBe("introduction-to-html");
    expect(set.challenges.length).toBeGreaterThan(0);

    expect(() => getPracticeSet(TRACK, COURSE, "html-foundations", "no-such-practice")).toThrow(
      /Practice set not found/,
    );
  });

  it("loads practice challenges in declared order with tests and levels", () => {
    const challenges = getPracticeChallenges(
      TRACK,
      COURSE,
      "html-foundations",
      "html-structure-practice",
    );
    expect(challenges.map((c) => c.id)).toEqual([
      "practice-minimal-document",
      "practice-titled-page",
      "practice-heading-hierarchy",
      "practice-article-structure",
    ]);
    for (const c of challenges) {
      expect(c.tests.length).toBeGreaterThan(0);
      expect(c.tests[0]?.hint).toBeTruthy();
      expect(c.level).toBeTruthy();
    }
  });

  it("resolves a single practice challenge with practice-set location", () => {
    const challenge = getPracticeChallenge(
      TRACK,
      COURSE,
      "css-foundations",
      "css-flexbox-practice",
      "flex-the-navbar",
    );
    expect(challenge.lessonId).toBe("css-flexbox-practice");
    expect(challenge.moduleId).toBe("css-foundations");
    expect(challenge.trackId).toBe(TRACK);
    expect(challenge.level).toBe("guided");

    expect(() =>
      getPracticeChallenge(TRACK, COURSE, "css-foundations", "css-flexbox-practice", "nope"),
    ).toThrow(/Challenge not found/);
  });

  it("interleaves lessons and anchored practice sets in module flow", () => {
    const flow = getModuleFlow(TRACK, COURSE, "html-foundations");
    const kinds = flow.map((step) => step.kind);
    // First lesson is immediately followed by its anchored practice.
    expect(kinds.slice(0, 2)).toEqual(["lesson", "practice"]);
    expect(flow[0]?.kind === "lesson" && flow[0].lesson.id).toBe("introduction-to-html");
    expect(flow[1]?.kind === "practice" && flow[1].practiceSet.id).toBe(
      "introduction-to-html-practice",
    );
    // Every practice set appears exactly once, lessons keep their order.
    const practiceIds = flow
      .filter(
        (s): s is Extract<(typeof flow)[number], { kind: "practice" }> => s.kind === "practice",
      )
      .map((s) => s.practiceSet.id);
    expect(new Set(practiceIds).size).toBe(practiceIds.length);
    const lessonIds = flow
      .filter((s): s is Extract<(typeof flow)[number], { kind: "lesson" }> => s.kind === "lesson")
      .map((s) => s.lesson.id);
    expect(lessonIds[0]).toBe("introduction-to-html");
  });

  it("covers the whole course: 52 practice sets, all challenges leveled", () => {
    let sets = 0;
    let leveled = 0;
    let total = 0;
    for (const moduleId of [
      "the-web-and-your-first-website",
      "how-modern-websites-work",
      "html-foundations",
      "css-foundations",
      "javascript-foundations",
      "developer-tools-git-and-github",
      "final-project",
    ]) {
      for (const p of getModulePractices(TRACK, COURSE, moduleId)) {
        sets += 1;
        const challenges = getPracticeChallenges(TRACK, COURSE, moduleId, p.id);
        total += challenges.length;
        leveled += challenges.filter((c) => c.level).length;
      }
    }
    expect(sets).toBe(52);
    expect(total).toBe(88);
    expect(leveled).toBe(88);
  });
});
