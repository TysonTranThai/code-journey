/**
 * Smoke: load the hsg-intermediate course through the REAL curriculum
 * loaders and print counts (modules/lessons/practices/challenges/minutes).
 * Also verifies EN + VI loads and per-module challenge sums.
 */
import {
  getTrack,
  getCourse,
  getCurriculumModule,
  getModulePractices,
  getPracticeChallenges,
} from "../../src/lib/curriculum/loaders.ts";

const track = getTrack("hsg");
console.log(
  "track:",
  track.id,
  "courses:",
  track.courses.map((c) => ("reference" in c ? c.reference : c.id)),
);

const course = getCourse("hsg", "hsg-intermediate");
console.log("course:", course.id, "modules:", course.modules.length);

let lessons = 0;
let practices = 0;
let challenges = 0;
let lessonMin = 0;
let practiceMin = 0;
for (const modRef of course.modules) {
  const moduleId = "reference" in modRef ? modRef.reference : modRef.id;
  const mod = getCurriculumModule("hsg", "hsg-intermediate", moduleId);
  lessons += mod.lessons.length;
  lessonMin += mod.lessons.reduce((a, l) => a + (l.minutes ?? 0), 0);
  const sets = getModulePractices("hsg", "hsg-intermediate", moduleId);
  for (const s of sets) {
    practices += 1;
    practiceMin += s.minutes ?? 0;
    const chs = getPracticeChallenges("hsg", "hsg-intermediate", moduleId, s.id);
    challenges += chs.length;
  }
}
console.log(
  "modules:",
  course.modules.length,
  "lessons:",
  lessons,
  "practices:",
  practices,
  "challenges:",
  challenges,
);
console.log(
  "lesson minutes:",
  lessonMin,
  "practice minutes:",
  practiceMin,
  "total hours:",
  Math.round((lessonMin + practiceMin) / 6) / 100,
);

// VI locale must load too
const courseVi = getCourse("hsg", "hsg-intermediate", undefined, "vi");
console.log("vi course title:", courseVi.title ?? "(vi overlay)");
