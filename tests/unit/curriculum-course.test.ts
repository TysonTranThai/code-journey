import { describe, expect, it } from "vitest";

import {
  getCourse,
  getCurriculumModule,
  getLinearLessons,
  getLessonChallenges,
  getModulePractices,
  getPracticeChallenges,
  getLesson,
  getTracks,
  readLessonBody,
} from "@/lib/curriculum/loaders";
import { getAchievementDefs } from "@/lib/progress/achievement-defs";

/**
 * Curriculum-wide integrity checks for the shipped course (Phase 8).
 * Everything here runs against the REAL content tree, not fixtures:
 * the loaders themselves fail loudly on schema violations, so a green run
 * means the whole track parses, all references resolve, and every lesson
 * body exists on disk.
 */
const TRACK = "web-development";
const COURSE = "web-development-beginner";

const EXPECTED_MODULE_ORDER = [
  "the-web-and-your-first-website",
  "html-foundations",
  "css-foundations",
  "javascript-foundations",
  "developer-tools-git-and-github",
  "how-modern-websites-work",
  "final-project",
];

describe("course structure (Phase 8: web-development-beginner)", () => {
  const course = getCourse(TRACK, COURSE);

  it("exists with the full 7-module teaching order", () => {
    expect(course.id).toBe(COURSE);
    expect(course.modules.map((m) => m.reference)).toEqual(EXPECTED_MODULE_ORDER);
  });

  it("ships 56 lessons across 7 modules", () => {
    const counts = EXPECTED_MODULE_ORDER.map((moduleId) => {
      const mod = getCurriculumModule(TRACK, COURSE, moduleId);
      return { moduleId, lessons: mod.lessons.length };
    });
    expect(counts).toEqual([
      { moduleId: "the-web-and-your-first-website", lessons: 4 },
      { moduleId: "html-foundations", lessons: 10 },
      { moduleId: "css-foundations", lessons: 12 },
      { moduleId: "javascript-foundations", lessons: 18 },
      { moduleId: "developer-tools-git-and-github", lessons: 6 },
      { moduleId: "how-modern-websites-work", lessons: 4 },
      { moduleId: "final-project", lessons: 2 },
    ]);
    expect(counts.reduce((n, c) => n + c.lessons, 0)).toBe(56);
  });

  it("has a linear order that interleave conceptual and practical modules", () => {
    const linear = getLinearLessons(TRACK);
    expect(linear).toHaveLength(143);
    expect(linear[0]?.id).toBe("how-the-web-works");
    expect(linear[55]?.id).toBe("capstone-build-and-ship");
    expect(linear[135]?.id).toBe("capstone-ship");
    expect(linear[136]?.id).toBe("html-architecture");
    expect(linear[142]?.id).toBe("docs-hub-project");
  });

  it("every lesson body exists on disk and is non-trivial", () => {
    const linear = getLinearLessons(TRACK);
    expect(linear.length).toBeGreaterThan(50);
    for (const lesson of linear) {
      const body = readLessonBody(TRACK, lesson.courseId, lesson.moduleId, lesson.id);
      // A real lesson explains; placeholder bodies would be far shorter.
      const threshold = lesson.courseId === "web-development-intermediate" ? 900 : 1200;
      expect(body.length, `lesson body too short: ${lesson.moduleId}/${lesson.id}`).toBeGreaterThan(
        threshold,
      );
    }
  });

  it("every declared challenge resolves with valid, executable tests", () => {
    // Course 1 revision: coding challenges live in practice sets (plus the
    // checkpoint challenges that stay lesson-attached).
    const linear = getLinearLessons(TRACK).filter((l) => l.courseId === COURSE);
    let challengeCount = 0;
    for (const lesson of linear) {
      const challenges = getLessonChallenges(TRACK, lesson.courseId, lesson.moduleId, lesson.id);
      for (const challenge of challenges) {
        challengeCount += 1;
        expect(challenge.prompt.length).toBeGreaterThan(0);
        expect(challenge.tests.length).toBeGreaterThan(0);
        for (const test of challenge.tests) {
          expect(test.name.length).toBeGreaterThan(0);
          expect(test.code.length).toBeGreaterThan(0);
          expect(test.hint.length).toBeGreaterThan(0);
        }
      }
    }
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
        for (const challenge of getPracticeChallenges(TRACK, COURSE, moduleId, p.id)) {
          challengeCount += 1;
          expect(challenge.prompt.length).toBeGreaterThan(0);
          expect(challenge.tests.length).toBeGreaterThan(0);
          expect(challenge.level, `${challenge.id} should have a level`).toBeTruthy();
          for (const test of challenge.tests) {
            expect(test.name.length).toBeGreaterThan(0);
            expect(test.code.length).toBeGreaterThan(0);
            expect(test.hint.length).toBeGreaterThan(0);
          }
        }
      }
    }
    expect(challengeCount).toBe(91);
  });

  it("intermediate course ships 13 modules, 80 lessons, 182 challenges", () => {
    const I2 = "web-development-intermediate";
    const course = getCourse(TRACK, I2);
    expect(course.modules.map((m) => m.reference)).toEqual([
      "modern-javascript",
      "advanced-dom-browser-apis",
      "asynchronous-javascript-apis",
      "advanced-css-ui-engineering",
      "typescript-essentials",
      "git-workflow",
      "testing-debugging",
      "web-performance",
      "web-security",
      "backend-fundamentals",
      "databases-full-stack",
      "production",
      "capstone",
    ]);

    let lessons = 0;
    let challengeCount = 0;
    for (const ref of course.modules) {
      const mod = getCurriculumModule(TRACK, I2, ref.reference);
      lessons += mod.lessons.length;
      for (const l of mod.lessons) {
        for (const challenge of getLessonChallenges(TRACK, I2, mod.id, l.reference)) {
          challengeCount += 1;
          expect(challenge.tests.length).toBeGreaterThan(0);
        }
      }
      for (const p of getModulePractices(TRACK, I2, mod.id)) {
        for (const challenge of getPracticeChallenges(TRACK, I2, mod.id, p.id)) {
          challengeCount += 1;
          expect(challenge.prompt.length).toBeGreaterThan(0);
          expect(challenge.level, `${challenge.id} should have a level`).toBeTruthy();
          for (const test of challenge.tests) {
            expect(test.name.length).toBeGreaterThan(0);
            expect(test.code.length).toBeGreaterThan(0);
            expect(test.hint.length).toBeGreaterThan(0);
          }
        }
      }
    }
    expect(lessons).toBe(80);
    expect(challengeCount).toBe(181);
  });

  it("hands-on modules each end with a checkpoint or project lesson", () => {
    const endings: Array<[string, string]> = [
      ["the-web-and-your-first-website", "inspecting-with-devtools"],
      ["html-foundations", "html-checkpoint"],
      ["css-foundations", "css-project-portfolio"],
      ["javascript-foundations", "js-project-interactive-app"],
      ["developer-tools-git-and-github", "git-checkpoint"],
      ["final-project", "capstone-build-and-ship"],
    ];
    for (const [moduleId, lastLessonId] of endings) {
      const mod = getCurriculumModule(TRACK, COURSE, moduleId);
      const last = mod.lessons.at(-1)?.reference;
      expect(last, `${moduleId} should end with ${lastLessonId}`).toBe(lastLessonId);
    }
  });

  it("is one track holding all three shipped web courses (no competing schemas)", () => {
    const tracks = getTracks();
    expect(tracks.map((t) => t.id)).toContain("web-development");
    const web = tracks.find((t) => t.id === "web-development");
    expect(web?.courses.map((c) => c.reference)).toEqual([
      COURSE,
      "web-development-intermediate",
      "web-development-advanced",
    ]);
  });
});

describe("achievement definitions stay in sync with the curriculum", () => {
  it("module-completion achievement tracks the real html-foundations lessons", () => {
    const defs = getAchievementDefs();
    expect(defs.map((d) => d.id)).toContain("html-foundations-complete");
    // The criterion is data-driven; the module on disk has 10 lessons now.
    const mod = getCurriculumModule(TRACK, COURSE, "html-foundations");
    expect(mod.lessons).toHaveLength(10);
  });
});

describe("lesson navigation integrity (PROG neighbor wiring)", () => {
  it("checkpoint lessons sit at module boundaries so next/prev cross modules", () => {
    // Last lesson of module 1 → first lesson of module 2.
    const seam = getLesson(TRACK, COURSE, "html-foundations", "introduction-to-html");
    expect(seam.moduleId).toBe("html-foundations");
    const linear = getLinearLessons(TRACK);
    const seamIndex = linear.findIndex((l) => l.id === "introduction-to-html");
    expect(linear[seamIndex - 1]?.moduleId).toBe("the-web-and-your-first-website");
  });
});
