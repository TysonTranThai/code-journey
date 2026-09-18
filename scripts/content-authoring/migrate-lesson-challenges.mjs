/**
 * Course 1 revision, phase 2: move lesson-attached challenges into per-lesson
 * practice sets so every lesson is pure Learn and ALL coding lives in Practice.
 *
 * - For each lesson that has a `challenges/` dir, create a practice set
 *   `modules/<mod>/practices/<lessonId>-practice.json` (afterLesson = lessonId)
 *   and move its challenge JSONs into `.../practices/<setId>/challenges/`.
 * - Lessons that are CHECKPOINTS keep their challenges attached (they are the
 *   understanding checks; moving them would orphan their progress records).
 * - module.json: lessons[] left unchanged; practices[] gets the new set refs.
 * - lesson JSON: `challenges` field removed (it is being deleted from the schema).
 *
 * Challenge ids are PRESERVED, so progress records, harness solution maps,
 * and achievement references keep working without any data migration.
 *
 * Run: node scripts/content-authoring/migrate-lesson-challenges.mjs
 */
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  renameSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import path from "node:path";

const ROOT = "src/content/tracks/web-development/courses/web-development-beginner/modules";
// Checkpoints stay lesson-attached (kept against the spec's "checkpoints").
const CHECKPOINT_LESSONS = new Set([
  "html-checkpoint",
  "css-checkpoint",
  "git-checkpoint",
  "js-checkpoint",
]);

let moved = 0;
let setsCreated = 0;

for (const mod of readdirSync(ROOT)) {
  const lessonsDir = path.join(ROOT, mod, "lessons");
  if (!existsSync(lessonsDir)) continue;
  const practicesDir = path.join(ROOT, mod, "practices");
  mkdirSync(practicesDir, { recursive: true });

  for (const entry of readdirSync(lessonsDir)) {
    if (!entry.endsWith(".json")) continue;
    const lessonPath = path.join(lessonsDir, entry);
    const lesson = JSON.parse(readFileSync(lessonPath, "utf8"));
    const srcChDir = path.join(lessonsDir, lesson.id, "challenges");

    if (!existsSync(srcChDir) || CHECKPOINT_LESSONS.has(lesson.id)) continue;
    const challengeFiles = readdirSync(srcChDir).filter((f) => f.endsWith(".json"));
    if (challengeFiles.length === 0) continue;

    // Practice set id = <lessonId>-practice (mirrors existing convention).
    const setId = `${lesson.id}-practice`;
    const setDir = path.join(practicesDir, setId);
    mkdirSync(path.join(setDir, "challenges"), { recursive: true });

    for (const cf of challengeFiles) {
      renameSync(path.join(srcChDir, cf), path.join(setDir, "challenges", cf));
      moved++;
    }
    rmSync(srcChDir, { recursive: true, force: true });

    const minutes = Math.max(5, Math.round(((lesson.minutes ?? 10) * 0.6) / 5) * 5);
    writeFileSync(
      path.join(practicesDir, `${setId}.json`),
      JSON.stringify(
        {
          id: setId,
          title: `${lesson.title} — Practice`,
          description: `Hands-on practice for “${lesson.title}”: apply what you just learned in ${lesson.id}.`,
          afterLesson: lesson.id,
          minutes,
          difficulty: lesson.difficulty ?? "beginner",
          challenges: challengeFiles.map(
            (f) => JSON.parse(readFileSync(path.join(setDir, "challenges", f), "utf8")).id,
          ),
        },
        null,
        2,
      ) + "\n",
    );
    setsCreated++;

    // Patch module.json: append practice ref.
    const modJsonPath = path.join(ROOT, mod, "module.json");
    const modJson = JSON.parse(readFileSync(modJsonPath, "utf8"));
    if (!modJson.practices) modJson.practices = [];
    if (!modJson.practices.some((p) => p.reference === setId)) {
      modJson.practices.push({ reference: setId });
      writeFileSync(modJsonPath, JSON.stringify(modJson, null, 2) + "\n");
    }
  }

  // Strip `challenges` from every lesson JSON in this module (schema drops it).
  for (const entry of readdirSync(lessonsDir)) {
    if (!entry.endsWith(".json")) continue;
    const lp = path.join(lessonsDir, entry);
    const lesson = JSON.parse(readFileSync(lp, "utf8"));
    if (!("challenges" in lesson)) continue;
    delete lesson.challenges;
    writeFileSync(lp, JSON.stringify(lesson, null, 2) + "\n");
  }
}

console.log(`Migration complete: ${moved} challenges moved, ${setsCreated} practice sets created`);
