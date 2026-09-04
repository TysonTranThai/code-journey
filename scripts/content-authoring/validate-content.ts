/**
 * Content validation: walk the whole track via the public loaders, count
 * lessons/challenges per module, and verify every declared challenge resolves.
 * Run: npx tsx scripts/content-authoring/validate-content.ts
 */
import {
  getCourse,
  getCurriculumModule,
  getLinearLessons,
  getLessonChallenges,
} from "@/lib/curriculum/loaders";

const courseId = "web-development-beginner";
const course = getCourse("web-development", courseId);
const linear = getLinearLessons("web-development");

let lessons = 0;
let challenges = 0;

for (const ref of course.modules) {
  const mod = getCurriculumModule("web-development", courseId, ref.reference);
  let moduleChallenges = 0;
  for (const l of mod.lessons) {
    const list = getLessonChallenges("web-development", courseId, mod.id, l.reference);
    if (list.length === 0) console.log(`    (no challenges: ${l.reference})`);
    moduleChallenges += list.length;
  }
  lessons += mod.lessons.length;
  challenges += moduleChallenges;
  console.log(`${mod.id} — ${mod.lessons.length} lessons, ${moduleChallenges} challenges`);
}

console.log(`\nLinear path: ${linear.length} lessons across the track`);
console.log(
  `TOTAL: ${course.modules.length} modules, ${lessons} lessons, ${challenges} challenges`,
);
