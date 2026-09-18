/**
 * Content validation for the C# — Advanced course (csharp-advanced) only.
 *
 * Mirrors validate-content.ts but loads through a scoped curriculum root
 * (a temp dir whose symlinked `tracks` dir exposes just the csharp track) so
 * that in-flight, broken state from OTHER agents' tracks never blocks this
 * QA pass. Every check runs through the real public loaders (schema +
 * overlays) in BOTH locales.
 *
 * Run: node --import tsx scripts/content-authoring/validate-content-csa.ts
 */
import {
  getChallenge,
  getCourse,
  getCurriculumModule,
  getLesson,
  getLessonChallenges,
  getLessonPractices,
  getPracticeChallenge,
  getPracticeChallenges,
  getPracticeSet,
} from "@/lib/curriculum/loaders";
import { mkdtempSync, mkdirSync, copyFileSync, symlinkSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const TRACK = "csharp";
const COURSE = "csharp-advanced";

// Scoped root: <tmp>/csharp/{track.json copy, courses -> real courses dir}.
// (loadCurriculum treats the root as the tracks dir and SKIPS symlinked
// track dirs — Dirent.isDirectory() is false for symlinks — so the track
// itself must be a real directory with only its courses symlinked.)
const root = mkdtempSync(path.join(tmpdir(), "csa-validate-"));
const trackDir = path.join(root, "csharp");
mkdirSync(trackDir);
copyFileSync("src/content/tracks/csharp/track.json", path.join(trackDir, "track.json"));
symlinkSync(
  path.resolve("src/content/tracks/csharp/courses"),
  path.join(trackDir, "courses"),
  "dir",
);

let failed = false;
const fail = (msg: string) => {
  console.log(`  FAIL ${msg}`);
  failed = true;
};

try {
  const course = getCourse(TRACK, COURSE, root);
  console.log(`=== ${COURSE} ===`);
  console.log(`modules: ${course.modules.length}, title: ${course.title}`);
  if (course.title !== "C# — Advanced") fail(`course title: ${course.title}`);
  if (course.modules.length !== 23) fail(`module count ${course.modules.length} != 23`);

  let lessons = 0;
  let challenges = 0;

  for (const ref of course.modules) {
    const mod = getCurriculumModule(TRACK, COURSE, ref.reference, root);
    let moduleChallenges = 0;
    for (const l of mod.lessons) {
      lessons++;
      const list = getLessonChallenges(TRACK, COURSE, mod.id, l.reference, root);
      moduleChallenges += list.length;
      challenges += list.length;
    }
    for (const p of mod.practices) {
      for (const c of getPracticeChallenges(TRACK, COURSE, mod.id, p.reference, root)) {
        moduleChallenges++;
        challenges++;
        void c;
      }
    }
    console.log(`  ${mod.id}: ${mod.lessons.length} lessons, ${moduleChallenges} challenges`);
  }
  console.log(`TOTAL: ${course.modules.length} modules, ${lessons} lessons, ${challenges} challenges`);

  // ── Locale sweep: every node must load through the schema-validating ────
  // loaders in BOTH locales.
  for (const locale of ["en", "vi"] as const) {
    let loads = 0;
    const tryLoad = (what: string, fn: () => unknown) => {
      try {
        fn();
        loads++;
      } catch (e) {
        fail(`LOCALE[${locale}] ${what}: ${e instanceof Error ? e.message : e}`);
      }
    };
    tryLoad("course", () => getCourse(TRACK, COURSE, root, locale));
    for (const ref of getCourse(TRACK, COURSE, root).modules) {
      const m = ref.reference;
      tryLoad(`${m}/module`, () => getCurriculumModule(TRACK, COURSE, m, root, locale));
      for (const lref of getCurriculumModule(TRACK, COURSE, m, root).lessons) {
        const lid = lref.reference;
        tryLoad(`${m}/${lid}/lesson`, () => getLesson(TRACK, COURSE, m, lid, root, locale));
        for (const p of getLessonPractices(TRACK, COURSE, m, lid, root)) {
          const pid = (p as { id?: string }).id ?? "";
          if (pid) {
            tryLoad(`${m}/${pid}/practice-set`, () =>
              getPracticeSet(TRACK, COURSE, m, pid, root, locale),
            );
          }
        }
        for (const c of getLessonChallenges(TRACK, COURSE, m, lid, root)) {
          tryLoad(`${m}/${lid}/${c.id}/challenge`, () =>
            getChallenge(TRACK, COURSE, m, lid, c.id, root, locale),
          );
        }
      }
      for (const pref of getCurriculumModule(TRACK, COURSE, m, root).practices) {
        const pid = pref.reference;
        tryLoad(`${m}/${pid}/practice-set`, () =>
          getPracticeSet(TRACK, COURSE, m, pid, root, locale),
        );
        for (const c of getPracticeChallenges(TRACK, COURSE, m, pid, root)) {
          tryLoad(`${m}/${pid}/${c.id}/challenge`, () =>
            getPracticeChallenge(TRACK, COURSE, m, pid, c.id, root, locale),
          );
        }
      }
    }
    if (locale === "vi" && loads < 200) fail(`vi locale loaded only ${loads} nodes`);
    console.log(`LOCALE: ${locale} — ${loads} nodes load clean`);
  }
} catch (e) {
  fail(`course load: ${e instanceof Error ? e.stack : e}`);
} finally {
  rmSync(root, { recursive: true, force: true });
}

if (failed) process.exit(1);
console.log("csharp-advanced: ALL CHECKS PASS");
