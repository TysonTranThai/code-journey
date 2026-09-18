import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { afterAll, describe, expect, it } from "vitest";

import {
  getChallenge,
  getLesson,
  getLessonPractices,
  getPracticeChallenge,
  getTracks,
  readLessonBody,
} from "@/lib/curriculum/loaders";
import { getLessonMdx } from "@/lib/curriculum/mdx-map";
import { DEFAULT_LOCALE } from "@/lib/i18n/config";

/**
 * Vietnamese content sidecars: `*.vi.json` overlays learner-facing text and
 * `*.vi.mdx` swaps the lesson body. English stays the structural source of
 * truth — ids, references, test code, and boilerplate never come from a
 * sidecar. Missing sidecars fall back to English per field/file.
 */

const tmpRoot = mkdtempSync(path.join(tmpdir(), "cj-vi-content-"));

// Minimal track: track → course → module → lesson (+ vi sidecars) and a
// practice set with one challenge (+ vi sidecar).
const trackDir = path.join(tmpRoot, "web-dev");
const courseDir = path.join(trackDir, "courses", "c1");
const moduleDir = path.join(courseDir, "modules", "m1");
const lessonsDir = path.join(moduleDir, "lessons");
mkdirSync(path.join(lessonsDir, "l1", "challenges"), { recursive: true });
mkdirSync(path.join(moduleDir, "practices", "p1", "challenges"), { recursive: true });

writeFileSync(
  path.join(trackDir, "track.json"),
  JSON.stringify({
    id: "web-dev",
    title: "Web Dev",
    description: "Track description",
    courses: [{ reference: "c1" }],
  }),
);
writeFileSync(
  path.join(courseDir, "course.json"),
  JSON.stringify({
    id: "c1",
    title: "Course One",
    description: "Course description",
    audience: "Beginners",
    outcomes: ["Build pages"],
    modules: [{ reference: "m1" }],
  }),
);
writeFileSync(
  path.join(moduleDir, "module.json"),
  JSON.stringify({
    id: "m1",
    title: "Module One",
    summary: "Module summary",
    lessons: [{ reference: "l1" }],
    practices: [{ reference: "p1" }],
  }),
);
writeFileSync(
  path.join(lessonsDir, "l1.json"),
  JSON.stringify({
    id: "l1",
    title: "Lesson One",
    description: "Lesson description",
    minutes: 5,
    difficulty: "beginner",
    contentPath: "./l1.mdx",
  }),
);
writeFileSync(path.join(lessonsDir, "l1.mdx"), "## English body\n\nHello.\n");
writeFileSync(path.join(lessonsDir, "l1.vi.mdx"), "## Nội dung tiếng Việt\n\nXin chào.\n");
writeFileSync(
  path.join(lessonsDir, "l1", "challenges", "chk.json"),
  JSON.stringify({
    id: "chk",
    title: "Checkpoint",
    prompt: "Fix the checkpoint.",
    difficulty: "beginner",
    boilerplate: "",
    tests: [{ name: "works", code: "if (!code.includes('a')) throw new Error('no');", hint: "Add a." }],
  }),
);
writeFileSync(
  path.join(moduleDir, "practices", "p1.json"),
  JSON.stringify({
    id: "p1",
    title: "Practice One",
    description: "Drill the basics",
    afterLesson: "l1",
    minutes: 10,
    difficulty: "beginner",
    challenges: ["ex1"],
  }),
);
writeFileSync(
  path.join(moduleDir, "practices", "p1", "challenges", "ex1.json"),
  JSON.stringify({
    id: "ex1",
    title: "Exercise One",
    prompt: "Print hello.",
    difficulty: "beginner",
    level: "imitation",
    boilerplate: "",
    tests: [
      { name: "prints", code: "if (!code.includes('hello')) throw new Error('say hello');", hint: "Use console.log." },
      { name: "short", code: "if (code.length > 100) throw new Error('too long');", hint: "Keep it short." },
    ],
  }),
);

// Vietnamese sidecars — title/prompt/hints only; test code stays English.
writeFileSync(path.join(trackDir, "track.vi.json"), JSON.stringify({ title: "Lập trình Web", description: "Mô tả track" }));
writeFileSync(
  path.join(courseDir, "course.vi.json"),
  JSON.stringify({
    title: "Khóa một",
    description: "Mô tả khóa",
    audience: "Người mới bắt đầu",
    outcomes: ["Xây dựng trang web"],
  }),
);
writeFileSync(path.join(moduleDir, "module.vi.json"), JSON.stringify({ title: "Mô-đun một", summary: "Tóm tắt" }));
writeFileSync(
  path.join(lessonsDir, "l1.vi.json"),
  JSON.stringify({ title: "Bài học một", description: "Mô tả bài học" }),
);
writeFileSync(
  path.join(lessonsDir, "l1", "challenges", "chk.vi.json"),
  JSON.stringify({ title: "Kiểm tra", prompt: "Sửa bài kiểm tra." }),
);
writeFileSync(
  path.join(moduleDir, "practices", "p1.vi.json"),
  JSON.stringify({ title: "Luyện tập một", description: "Rèn kỹ năng cơ bản" }),
);
writeFileSync(
  path.join(moduleDir, "practices", "p1", "challenges", "ex1.vi.json"),
  JSON.stringify({
    title: "Bài tập một",
    prompt: "In ra lời chào.",
    tests: [
      { name: "in ra", hint: "Dùng console.log." },
      { hint: "Giữ ngắn gọn." },
    ],
  }),
);

afterAll(() => {
  rmSync(tmpRoot, { recursive: true, force: true });
});

describe("curriculum Vietnamese sidecars", () => {
  it("defaults to English when no locale is passed", () => {
    const track = getTracks(tmpRoot)[0]!;
    expect(track.title).toBe("Web Dev");
  });

  it("overlays track/course/module/lesson text for vi", () => {
    const track = getTracks(tmpRoot, "vi")[0]!;
    expect(track.title).toBe("Lập trình Web");
    expect(track.description).toBe("Mô tả track");

    const lesson = getLesson("web-dev", "c1", "m1", "l1", tmpRoot, "vi");
    expect(lesson.title).toBe("Bài học một");
    expect(lesson.description).toBe("Mô tả bài học");
    // Structural fields never come from the sidecar.
    expect(lesson.minutes).toBe(5);
    expect(lesson.difficulty).toBe("beginner");
  });

  it("overlays challenge title/prompt and merges test name/hint by index, never test code", () => {
    const challenge = getPracticeChallenge("web-dev", "c1", "m1", "p1", "ex1", tmpRoot, "vi");
    expect(challenge.title).toBe("Bài tập một");
    expect(challenge.prompt).toBe("In ra lời chào.");
    expect(challenge.tests[0]!.name).toBe("in ra");
    expect(challenge.tests[0]!.hint).toBe("Dùng console.log.");
    // Second test has no vi name — keeps the English name, vi hint.
    expect(challenge.tests[1]!.name).toBe("short");
    expect(challenge.tests[1]!.hint).toBe("Giữ ngắn gọn.");
    // Grading semantics untouched.
    expect(challenge.tests[0]!.code).toContain("code.includes('hello')");
    expect(challenge.boilerplate).toBe("");
  });

  it("checkpoint challenge sidecar resolves too", () => {
    const challenge = getChallenge("web-dev", "c1", "m1", "l1", "chk", tmpRoot, "vi");
    expect(challenge.title).toBe("Kiểm tra");
    expect(challenge.prompt).toBe("Sửa bài kiểm tra.");
  });

  it("falls back to English per-file and per-field", () => {
    // p1 has a vi sidecar; chk.vi.json covers only title/prompt — name/hint
    // stay English.
    const challenge = getChallenge("web-dev", "c1", "m1", "l1", "chk", tmpRoot, "vi");
    expect(challenge.tests[0]!.name).toBe("works");
    expect(challenge.tests[0]!.hint).toBe("Add a.");
  });

  it("swaps the lesson body to .vi.mdx when present, English otherwise", () => {
    expect(readLessonBody("web-dev", "c1", "m1", "l1", tmpRoot, "vi")).toContain("tiếng Việt");
    expect(readLessonBody("web-dev", "c1", "m1", "l1", tmpRoot, "en")).toContain("English body");
  });

  it("resolves the vi MDX component through the map with graceful fallback", () => {
    // Real lesson with no vi sidecar yet: vi lookup falls back to the English
    // component (partial translation never blanks a page).
    expect(getLessonMdx("./anatomy-of-a-website.mdx", "vi")).toBeDefined();
    expect(getLessonMdx("./anatomy-of-a-website.mdx", "en")).toBeDefined();
    // A lesson unknown in both locales stays undefined.
    expect(getLessonMdx("./no-such-lesson.mdx", "vi")).toBeUndefined();
  });

  it("keeps locale caches separate (en object is not the vi object)", () => {
    const en = getLesson("web-dev", "c1", "m1", "l1", tmpRoot, "en");
    const vi = getLesson("web-dev", "c1", "m1", "l1", tmpRoot, "vi");
    expect(en.title).not.toBe(vi.title);
    expect(en.id).toBe(vi.id);
  });

  it("practice sets resolve in vi with anchored afterLesson intact", () => {
    const practices = getLessonPractices("web-dev", "c1", "m1", "l1", tmpRoot, "vi");
    expect(practices[0]!.title).toBe("Luyện tập một");
    expect(practices[0]!.afterLesson).toBe("l1");
  });

  it("default locale constant is English", () => {
    expect(DEFAULT_LOCALE).toBe("en");
  });
});
