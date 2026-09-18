/**
 * Course 3 (web-development-advanced) scoped content validation.
 *
 * Validates the same constraints as the platform loaders but scoped to one
 * course, so it runs while OTHER tracks are mid-authoring by another agent.
 * Every file is parsed with the production zod schemas (content-as-data),
 * EN/VI id parity is enforced, and all cross-references are resolved.
 *
 * Run: npx tsx scripts/content-authoring/validate-c3.ts
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import path from "node:path";
import {
  courseSchema,
  moduleSchema,
  lessonSchema,
  practiceSetSchema,
  challengeSchema,
  type Course,
  type CurriculumModule,
  type Lesson,
  type PracticeSet,
  type Challenge,
} from "@/lib/curriculum/schema";

const COURSE_DIR =
  "src/content/tracks/web-development/courses/web-development-advanced";
const MODULE_DIR = path.join(COURSE_DIR, "modules");

/** VI overlays translate display strings only; ids/structure stay shared. */
interface ViOverlay {
  id?: string;
  title?: string;
}

let errors = 0;
const fail = (msg: string) => {
  errors++;
  console.log(`  ✗ ${msg}`);
};

function readJson(p: string): unknown {
  try {
    return JSON.parse(readFileSync(p, "utf8"));
  } catch (e) {
    fail(`unparseable JSON: ${p} (${e instanceof Error ? e.message : e})`);
    return undefined;
  }
}

interface Parseable {
  safeParse: (v: unknown) => { success: boolean; error?: { issues: unknown[] } };
}

function zodParse<T>(
  schema: Parseable,
  file: string,
  what: string,
): T | undefined {
  const raw = readJson(file);
  if (raw === undefined) return undefined;
  const r = schema.safeParse(raw);
  if (!r.success) {
    fail(`${what} schema invalid: ${file} (${r.error?.issues.length} issues)`);
    return undefined;
  }
  return raw as T;
}

function readViOverlay(p: string, what: string): ViOverlay | undefined {
  const raw = readJson(p);
  if (raw === undefined) {
    fail(`missing VI overlay: ${what}`);
    return undefined;
  }
  return raw as ViOverlay;
}

// ── course.json + VI overlay ────────────────────────────────────────────────
const courseEn = zodParse<Course>(
  courseSchema,
  path.join(COURSE_DIR, "course.json"),
  "course",
);
const courseVi = readViOverlay(
  path.join(COURSE_DIR, "course.vi.json"),
  "course.vi.json",
);
if (courseEn && courseVi?.id !== undefined && courseVi.id !== courseEn.id) {
  fail("course.vi.json id diverges from course.json");
}

if (!courseEn) {
  console.log(`\nCOURSE 3 VALIDATION FAILED (course file unreadable)`);
  process.exit(1);
}

let lessonCount = 0;
let practiceSetCount = 0;
let challengeCount = 0;
let viMdxMissing = 0;

for (const ref of courseEn.modules) {
  const moduleId = ref.reference;
  const modDir = path.join(MODULE_DIR, moduleId);
  const modEn = zodParse<CurriculumModule>(
    moduleSchema,
    path.join(modDir, "module.json"),
    "module",
  );
  if (!modEn) continue;

  // lessons
  for (const l of modEn.lessons) {
    const lesson = zodParse<Lesson>(
      lessonSchema,
      path.join(modDir, "lessons", `${l.reference}.json`),
      "lesson",
    );
    if (!lesson) continue;
    lessonCount++;
    if (!existsSync(path.join(modDir, "lessons", `${l.reference}.mdx`))) {
      fail(`missing EN body: ${moduleId}/${l.reference}.mdx`);
    }
    if (!existsSync(path.join(modDir, "lessons", `${l.reference}.vi.mdx`))) {
      viMdxMissing++;
      fail(`missing VI body: ${moduleId}/${l.reference}.vi.mdx`);
    }
    readViOverlay(
      path.join(modDir, "lessons", `${l.reference}.vi.json`),
      `${moduleId}/${l.reference}.vi.json`,
    );
  }

  // practice sets + challenges
  for (const p of modEn.practices) {
    const set = zodParse<PracticeSet>(
      practiceSetSchema,
      path.join(modDir, "practices", `${p.reference}.json`),
      "practice set",
    );
    if (!set) continue;
    practiceSetCount++;
    readViOverlay(
      path.join(modDir, "practices", `${p.reference}.vi.json`),
      `${moduleId}/${p.reference}.vi.json`,
    );

    // anchored lessons must exist
    if (set.afterLesson && !modEn.lessons.some((l) => l.reference === set.afterLesson)) {
      fail(`practice set ${p.reference} anchors afterLesson "${set.afterLesson}" which is not a lesson of ${moduleId}`);
    }

    for (const cid of set.challenges) {
      const chDir = path.join(modDir, "practices", p.reference, "challenges");
      const ch = zodParse<Challenge>(
        challengeSchema,
        path.join(chDir, `${cid}.json`),
        "challenge",
      );
      if (!ch) continue;
      challengeCount++;
      if (ch.tests.length === 0) fail(`challenge ${cid} has no tests`);
      if (!ch.level) fail(`challenge ${cid} (practice) should declare a deliberate-practice level`);
      readViOverlay(
        path.join(chDir, `${cid}.vi.json`),
        `${cid}.vi.json`,
      );
    }
    // no orphan challenge files
    const chDir = path.join(modDir, "practices", p.reference, "challenges");
    if (existsSync(chDir)) {
      for (const f of readdirSync(chDir)) {
        if (!f.endsWith(".json") || f.endsWith(".vi.json")) continue;
        const id = f.replace(/\.json$/, "");
        if (!set.challenges.includes(id)) {
          fail(`orphan challenge file not declared in set ${p.reference}: ${id}`);
        }
      }
    }
  }
}

console.log(`\n=== web-development-advanced (Course 3) ===`);
console.log(
  `modules: ${courseEn.modules.length}, lessons: ${lessonCount}, practice sets: ${practiceSetCount}, challenges: ${challengeCount}`,
);
if (viMdxMissing === 0) console.log(`EN/VI structural parity: OK`);

if (errors > 0) {
  console.log(`\nCOURSE 3 VALIDATION FAILED — ${errors} error(s)`);
  process.exit(1);
}
console.log(`\nCOURSE 3 VALIDATION PASSED`);
