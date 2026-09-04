import path from "node:path";
import { describe, expect, it } from "vitest";

import {
  getChallenge,
  getLessonChallenges,
  getLinearLessons,
  getLinearNeighbors,
  getTracks,
  readLessonBody,
} from "@/lib/curriculum/loaders";

const FIXTURES = path.resolve(process.cwd(), "tests/fixtures/content-invalid");

function fixtureRoot(name: string): string {
  // Each case dir contains a tracks/ subdir (the loader's expected root).
  return path.join(FIXTURES, name, "tracks");
}

describe("curriculum loaders (real content)", () => {
  it("loads the course curriculum: 1 track, 56 linear lessons in spec order", () => {
    const tracks = getTracks();
    expect(tracks).toHaveLength(1);
    expect(tracks[0]?.id).toBe("web-development");

    const linear = getLinearLessons("web-development");
    expect(linear).toHaveLength(56);
    // Anchors at the seams between modules (the spec's teaching order).
    expect(linear[0]?.id).toBe("how-the-web-works");
    expect(linear[4]?.id).toBe("introduction-to-html");
    expect(linear[14]?.id).toBe("what-css-is");
    expect(linear[26]?.id).toBe("what-javascript-does");
    expect(linear[44]?.id).toBe("terminal-basics");
    expect(linear[54]?.id).toBe("capstone-planning");
    expect(linear[55]?.id).toBe("capstone-build-and-ship");
  });

  it("assigns linear indexes and resolves neighbors across the whole course", () => {
    const linear = getLinearLessons("web-development");
    expect(linear[0]?.linearIndex).toBe(0);
    expect(linear[55]?.linearIndex).toBe(55);

    const mid = getLinearNeighbors("web-development", "html-elements");
    expect(mid.prev?.id).toBe("introduction-to-html");
    expect(mid.next?.id).toBe("html-attributes");

    const first = getLinearNeighbors("web-development", "how-the-web-works");
    expect(first.prev).toBeNull();

    const last = getLinearNeighbors("web-development", "capstone-build-and-ship");
    expect(last.next).toBeNull();
  });

  it("throws CurriculumNotFoundError for unknown tracks/lessons", async () => {
    const { getTrack } = await import("@/lib/curriculum/loaders");
    expect(() => getTrack("does-not-exist")).toThrow(/Track not found/);
  });

  it("reads a lesson body that exists on disk", () => {
    const body = readLessonBody(
      "web-development",
      "web-development-beginner",
      "html-foundations",
      "introduction-to-html",
    );
    expect(body).toContain("HyperText Markup Language");
  });

  it("loads lesson challenges in declared order with resolved location", () => {
    const challenges = getLessonChallenges(
      "web-development",
      "web-development-beginner",
      "html-foundations",
      "introduction-to-html",
    );
    expect(challenges.map((c) => c.id)).toEqual(["fix-the-heading"]);
    expect(challenges[0]?.tests.length).toBeGreaterThan(0);
    expect(challenges[0]?.tests[0]?.hint).toBeTruthy();

    const resolved = getChallenge(
      "web-development",
      "web-development-beginner",
      "html-foundations",
      "html-links",
      "add-the-missing-link",
    );
    expect(resolved.lessonId).toBe("html-links");
    expect(resolved.trackId).toBe("web-development");
    expect(resolved.tests).toHaveLength(3);
  });

  it("throws for an unknown challenge id", () => {
    expect(() =>
      getChallenge(
        "web-development",
        "web-development-beginner",
        "html-foundations",
        "introduction-to-html",
        "no-such-challenge",
      ),
    ).toThrow(/Challenge not found/);
  });
});

describe("curriculum loaders (invalid content fails loudly)", () => {
  it("missing-required-field: lesson without minutes throws with file and issue", () => {
    expect(() => getTracks(fixtureRoot("missing-required-field"))).toThrow(
      /missing-required-field.*no-minutes\.json.*minutes/s,
    );
  });

  it("duplicate-lesson-id: same lesson id twice throws naming both files", () => {
    expect(() => getTracks(fixtureRoot("duplicate-lesson-id"))).toThrow(
      /duplicate id "shared-lesson"/,
    );
  });

  it("broken-content-path: unresolved contentPath throws naming the lesson file", () => {
    expect(() => getTracks(fixtureRoot("broken-content-path"))).toThrow(
      /contentPath "\.\/does-not-exist\.mdx" does not resolve/,
    );
  });

  it("empty-lessons-array: module with no lessons throws", () => {
    expect(() => getTracks(fixtureRoot("empty-lessons-array"))).toThrow(/at least one lesson/);
  });

  it("challenge-unknown-lesson: dangling challenge reference throws naming the lesson file", () => {
    expect(() => getTracks(fixtureRoot("challenge-unknown-lesson"))).toThrow(
      /challenge reference "no-such-challenge" has no file/,
    );
  });
});
