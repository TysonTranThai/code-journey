import { describe, expect, it } from "vitest";

import { courseSchema, lessonSchema, moduleSchema, trackSchema } from "@/lib/curriculum/schema";

const validLesson = {
  id: "introduction-to-html",
  title: "Introduction to HTML",
  description: "What HTML is and your first document.",
  minutes: 10,
  difficulty: "beginner",
  contentPath: "./introduction-to-html.mdx",
  challenges: [],
};

const validModule = {
  id: "html-foundations",
  title: "HTML Foundations",
  summary: "The building blocks of every web page.",
  lessons: [{ reference: "introduction-to-html" }],
};

const validCourse = {
  id: "web-development-foundations",
  title: "Web Development Foundations",
  description: "Your first course on real web pages.",
  modules: [{ reference: "html-foundations" }],
};

const validTrack = {
  id: "web-development",
  title: "Web Development",
  description: "Start your journey from zero.",
  courses: [{ reference: "web-development-foundations" }],
};

describe("curriculum schema (valid content)", () => {
  it("parses a valid lesson, module, course, and track", () => {
    expect(lessonSchema.parse(validLesson)).toMatchObject({ id: "introduction-to-html" });
    expect(moduleSchema.parse(validModule)).toMatchObject({ id: "html-foundations" });
    expect(courseSchema.parse(validCourse)).toMatchObject({
      id: "web-development-foundations",
    });
    expect(trackSchema.parse(validTrack)).toMatchObject({ id: "web-development" });
  });

  it("defaults challenges to an empty array when omitted", () => {
    const { challenges } = lessonSchema.parse({ ...validLesson, challenges: undefined });
    expect(challenges).toEqual([]);
  });
});

describe("curriculum schema (invalid content throws)", () => {
  it("rejects ids that are not lowercase slugs", () => {
    expect(() => lessonSchema.parse({ ...validLesson, id: "Bad Id" })).toThrow();
    expect(() => lessonSchema.parse({ ...validLesson, id: "UPPER" })).toThrow();
  });

  it("rejects out-of-range minutes", () => {
    expect(() => lessonSchema.parse({ ...validLesson, minutes: 0 })).toThrow();
    expect(() => lessonSchema.parse({ ...validLesson, minutes: 241 })).toThrow();
    expect(() => lessonSchema.parse({ ...validLesson, minutes: 1.5 })).toThrow();
  });

  it("rejects unknown difficulty values", () => {
    expect(() => lessonSchema.parse({ ...validLesson, difficulty: "expert" })).toThrow();
  });

  it("rejects lessons with a missing or empty title", () => {
    const missing = { ...validLesson } as Record<string, unknown>;
    delete missing.title;
    expect(() => lessonSchema.parse(missing)).toThrow();
    expect(() => lessonSchema.parse({ ...validLesson, title: "" })).toThrow();
  });

  it("rejects modules with an empty lessons array", () => {
    expect(() => moduleSchema.parse({ ...validModule, lessons: [] })).toThrow(
      /at least one lesson/i,
    );
  });

  it("rejects courses with no modules and tracks with no courses", () => {
    expect(() => courseSchema.parse({ ...validCourse, modules: [] })).toThrow(
      /at least one module/i,
    );
    expect(() => trackSchema.parse({ ...validTrack, courses: [] })).toThrow(/at least one course/i);
  });

  it("reports the failing field path in zod issues", () => {
    try {
      lessonSchema.parse({ ...validLesson, minutes: 999 });
      expect.unreachable("should have thrown");
    } catch (error) {
      const issues = (error as { issues: { path: unknown[] }[] }).issues;
      expect(issues[0]?.path).toContain("minutes");
    }
  });
});
