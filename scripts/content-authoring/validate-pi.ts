/**
 * Scoped validator — Python — Intermediate (schema + EN/VI parity).
 * Loads every course node through the platform's zod schemas in both locales.
 * Run: npx tsx scripts/content-authoring/validate-pi.ts
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";

import {
  challengeSchema,
  courseSchema,
  lessonSchema,
  moduleSchema,
  practiceSetSchema,
} from "../../src/lib/curriculum/schema";

const COURSE_DIR = path.join(
  "src/content/tracks/python/courses/python-intermediate",
);

type Issue = { file: string; error: string };

const issues: Issue[] = [];

function fail(file: string, error: unknown) {
  const msg =
    error && typeof error === "object" && "issues" in error
      ? JSON.stringify((error as { issues: unknown[] }).issues)
      : String(error);
  issues.push({ file, error: msg });
}

function readJson(file: string): unknown {
  return JSON.parse(readFileSync(file, "utf-8"));
}

const counts = {
  modules: 0,
  lessons: 0,
  practices: 0,
  challenges: 0,
  minutes: 0,
};

const courseEn = courseSchema.parse(readJson(path.join(COURSE_DIR, "course.json")));
const courseViRaw = readJson(path.join(COURSE_DIR, "course.vi.json")) as Record<string, unknown>;

// Course-level parity
if (courseViRaw["title"] === undefined || courseViRaw["description"] === undefined) {
  fail("course.vi.json", "missing title/description overlay");
}

for (const modRef of courseEn.modules) {
  const modDir = path.join(COURSE_DIR, "modules", modRef.reference);
  const moduleEn = moduleSchema.parse(readJson(path.join(modDir, "module.json")));
  counts.modules += 1;

  const viModulePath = path.join(modDir, "module.vi.json");
  if (!existsSync(viModulePath)) {
    fail(viModulePath, "missing VI module overlay");
  } else {
    const viModule = readJson(viModulePath) as Record<string, unknown>;
    if (!viModule["title"] || !viModule["summary"]) {
      fail(viModulePath, "incomplete VI module overlay");
    }
  }

  for (const lessonRef of moduleEn.lessons) {
    const lessonPath = path.join(modDir, "lessons", lessonRef.reference + ".json");
    const lessonEn = lessonSchema.parse(readJson(lessonPath));
    counts.lessons += 1;
    counts.minutes += lessonEn.minutes;

    const viLessonPath = path.join(modDir, "lessons", lessonRef.reference + ".vi.json");
    if (!existsSync(viLessonPath)) {
      fail(viLessonPath, "missing VI lesson overlay");
    } else {
      const viLesson = readJson(viLessonPath) as Record<string, unknown>;
      if (!viLesson["title"] || !viLesson["description"]) {
        fail(viLessonPath, "incomplete VI lesson overlay");
      }
    }

    const bodyPath = path.join(modDir, "lessons", lessonEn.contentPath.replace("./", ""));
    if (!existsSync(bodyPath)) fail(bodyPath, "missing EN lesson body");
    const viBodyPath = bodyPath.replace(/\.mdx$/, ".vi.mdx");
    if (!existsSync(viBodyPath)) fail(viBodyPath, "missing VI lesson body");

    // lesson-attached checkpoint challenges
    const chDir = path.join(modDir, "lessons", lessonRef.reference, "challenges");
    if (existsSync(chDir)) {
      for (const f of readdirSync(chDir)) {
        if (!f.endsWith(".json") || f.endsWith(".vi.json")) continue;
        const ch = challengeSchema.parse(readJson(path.join(chDir, f)));
        counts.challenges += 1;
        if (ch.language !== "python") fail(path.join(chDir, f), "expected language=python");
        const vi = path.join(chDir, f.replace(".json", ".vi.json"));
        if (!existsSync(vi)) fail(vi, "missing VI challenge overlay");
      }
    }
  }

  for (const practiceRef of moduleEn.practices) {
    const practicePath = path.join(modDir, "practices", practiceRef.reference + ".json");
    const practiceEn = practiceSetSchema.parse(readJson(practicePath));
    counts.practices += 1;
    counts.minutes += practiceEn.minutes;

    const viPracticePath = path.join(modDir, "practices", practiceRef.reference + ".vi.json");
    if (!existsSync(viPracticePath)) {
      fail(viPracticePath, "missing VI practice overlay");
    } else {
      const viPractice = readJson(viPracticePath) as Record<string, unknown>;
      if (!viPractice["title"] || !viPractice["description"]) {
        fail(viPracticePath, "incomplete VI practice overlay");
      }
    }

    for (const challengeId of practiceEn.challenges) {
      const chPath = path.join(
        modDir,
        "practices",
        practiceRef.reference,
        "challenges",
        challengeId + ".json",
      );
      const ch = challengeSchema.parse(readJson(chPath));
      counts.challenges += 1;
      if (ch.language !== "python") fail(chPath, "expected language=python");
      const vi = path.join(
        modDir,
        "practices",
        practiceRef.reference,
        "challenges",
        challengeId + ".vi.json",
      );
      if (!existsSync(vi)) fail(vi, "missing VI challenge overlay");
    }
  }
}

console.log(
  `python-intermediate: ${counts.modules} modules, ${counts.lessons} lessons, ` +
    `${counts.practices} practice sets, ${counts.challenges} challenges, ` +
    `${counts.minutes} scheduled minutes (≈${(counts.minutes / 60).toFixed(1)} h)`,
);

if (issues.length > 0) {
  console.error(`VALIDATION FAILED — ${issues.length} issue(s):`);
  for (const issue of issues) {
    console.error(`  ${issue.file}: ${issue.error}`);
  }
  process.exit(1);
}
console.log("VALIDATION PASSED — schema-valid in EN and VI, full structural parity.");
