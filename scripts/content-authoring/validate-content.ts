/**
 * Content validation: walk each course in the track via the public loaders,
 * count lessons/challenges per module, and verify every declared challenge
 * resolves. Also verifies EN/VI structural synchronization per course.
 * Run: npx tsx scripts/content-authoring/validate-content.ts
 */
import {
  getChallenge,
  getCourse,
  getCurriculumModule,
  getLinearLessons,
  getLessonChallenges,
  getLessonPractices,
  getPracticeChallenge,
  getPracticeChallenges,
  getPracticeSet,
  getLesson,
} from "@/lib/curriculum/loaders";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import path from "node:path";

const COURSE_TRACKS: Array<{ track: string; course: string }> = [
  { track: "web-development", course: "web-development-beginner" },
  { track: "web-development", course: "web-development-intermediate" },
  { track: "web-development", course: "web-development-advanced" },
  { track: "python", course: "python-beginner" },
  { track: "python", course: "python-intermediate" },
  { track: "python", course: "python-advanced" },
  { track: "cpp", course: "cpp-beginner" },
  { track: "cpp", course: "cpp-intermediate" },
  { track: "cpp", course: "cpp-advanced" },
  { track: "java", course: "java-beginner" },
  { track: "java", course: "java-intermediate" },
  { track: "java", course: "java-advanced" },
  { track: "c", course: "c-intermediate" },
  { track: "c", course: "c-advanced" },
  { track: "csharp", course: "csharp-beginner" },
  { track: "csharp", course: "csharp-intermediate" },
  { track: "csharp", course: "csharp-advanced" },
  { track: "hsg", course: "hsg-beginner" },
  { track: "ap-csa", course: "ap-csa-beginner" },
  { track: "ap-csa", course: "ap-csa-core" },
  { track: "ap-csa", course: "ap-csa-advanced" },
];
const baseDir = path.join("src/content/tracks");

let failed = false;

for (const { track: TRACK, course: courseId } of COURSE_TRACKS) {
  // Authoring shells (parseable course.json, empty modules array) are
  // skipped by the loaders (see loadTrack) so in-progress courses from other
  // agents never take the site down. Mirror that tolerance here with a
  // visible warning instead of crashing the whole QA pass.
  const courseJsonPath = path.join(baseDir, TRACK, "courses", courseId, "course.json");
  try {
    const raw = JSON.parse(readFileSync(courseJsonPath, "utf8")) as { modules?: unknown };
    if (Array.isArray(raw.modules) && raw.modules.length === 0) {
      console.log(`\n=== ${courseId} ===\n  (authoring shell — no modules yet, skipped)`);
      continue;
    }
  } catch {
    // course.json missing/unparseable → another agent may not have started
    // this course yet (e.g. ap-csa-core mid-authoring); warn and skip rather
    // than failing the whole QA pass for every other course.
    console.log(`\n=== ${courseId} ===\n  (course.json missing — course not authored yet, skipped)`);
    continue;
  }
  const course = getCourse(TRACK, courseId);
  let lessons = 0;
  let challenges = 0;
  const perCourse: string[] = [];

  for (const ref of course.modules) {
    const mod = getCurriculumModule(TRACK, courseId, ref.reference);
    let moduleChallenges = 0;
    for (const l of mod.lessons) {
      const list = getLessonChallenges(TRACK, courseId, mod.id, l.reference);
      if (list.length === 0) console.log(`    (no challenges: ${l.reference})`);
      moduleChallenges += list.length;
    }
    lessons += mod.lessons.length;
    challenges += moduleChallenges;
    perCourse.push(`${mod.id} — ${mod.lessons.length} lessons, ${moduleChallenges} challenges`);
  }

  console.log(`\n=== ${courseId} ===`);
  for (const line of perCourse) console.log(line);
  console.log(
    `TOTAL: ${course.modules.length} modules, ${lessons} lessons, ${challenges} challenges`,
  );

  // ── EN/VI structural synchronization ──────────────────────────────────────
  const courseDir = path.join(baseDir, TRACK, "courses", courseId, "modules");
  let viMismatches = 0;

  const checkPair = (enFile: string, viFile: string, what: string) => {
    if (!existsSync(viFile)) {
      console.log(`  SYNC MISSING VI ${what}`);
      viMismatches++;
      return;
    }
    const en = JSON.parse(readFileSync(enFile, "utf8"));
    const vi = JSON.parse(readFileSync(viFile, "utf8"));
    if (en.id !== undefined && vi.id !== undefined && en.id !== vi.id) {
      console.log(`  SYNC ID MISMATCH ${what}: ${en.id} vs ${vi.id}`);
      viMismatches++;
    }
  };

  for (const mod of readdirSync(courseDir)) {
    const modDir = path.join(courseDir, mod);
    checkPair(
      path.join(modDir, "module.json"),
      path.join(modDir, "module.vi.json"),
      `${mod}/module`,
    );
    const lessonsDir = path.join(modDir, "lessons");
    if (!existsSync(lessonsDir)) continue;
    for (const f of readdirSync(lessonsDir)) {
      if (!f.endsWith(".json") || f.endsWith(".vi.json")) continue;
      checkPair(
        path.join(lessonsDir, f),
        path.join(lessonsDir, f.replace(".json", ".vi.json")),
        `${mod}/${f}`,
      );
      const chDir = path.join(lessonsDir, f.replace(".json", ""), "challenges");
      if (existsSync(chDir)) {
        for (const c of readdirSync(chDir)) {
          if (!c.endsWith(".json") || c.endsWith(".vi.json")) continue;
          checkPair(
            path.join(chDir, c),
            path.join(chDir, c.replace(".json", ".vi.json")),
            `${mod}/${c}`,
          );
        }
      }
    }
    const practicesDir = path.join(modDir, "practices");
    if (!existsSync(practicesDir)) continue;
    for (const f of readdirSync(practicesDir)) {
      if (!f.endsWith(".json") || f.endsWith(".vi.json")) continue;
      checkPair(
        path.join(practicesDir, f),
        path.join(practicesDir, f.replace(".json", ".vi.json")),
        `${mod}/${f}`,
      );
      const chDir = path.join(practicesDir, f.replace(".json", ""), "challenges");
      if (existsSync(chDir)) {
        for (const c of readdirSync(chDir)) {
          if (!c.endsWith(".json") || c.endsWith(".vi.json")) continue;
          checkPair(
            path.join(chDir, c),
            path.join(chDir, c.replace(".json", ".vi.json")),
            `${mod}/${c}`,
          );
        }
      }
    }
  }

  if (viMismatches > 0) {
    console.log(`SYNC: ${viMismatches} EN/VI structural mismatches in ${courseId}`);
    failed = true;
  } else {
    console.log(`SYNC: EN/VI structures match for ${courseId}`);
  }

  // ── Locale sweep: every node must load through the schema-validating ────
  // loaders in BOTH locales (structural file sync alone cannot catch a VI
  // overlay that fails schema validation — e.g. an over-long string — which
  // only surfaces as a 404 at request time).
  for (const locale of ["en", "vi"] as const) {
    let loads = 0;
    let localeFailures = 0;
    const tryLoad = (what: string, fn: () => unknown) => {
      try {
        fn();
        loads++;
      } catch (e) {
        console.log(`  LOCALE[${locale}] FAIL ${what}: ${e instanceof Error ? e.message : e}`);
        localeFailures++;
      }
    };
    tryLoad(`${courseId}/course`, () => getCourse(TRACK, courseId, undefined, locale));
    for (const ref of getCourse(TRACK, courseId).modules) {
      const m = ref.reference;
      tryLoad(`${m}/module`, () => getCurriculumModule(TRACK, courseId, m, undefined, locale));
      for (const lref of getCurriculumModule(TRACK, courseId, m).lessons) {
        const lid = lref.reference;
        tryLoad(`${m}/${lid}/lesson`, () => getLesson(TRACK, courseId, m, lid, undefined, locale));
        for (const p of getLessonPractices(TRACK, courseId, m, lid)) {
          const pid = p.id ?? (p as { reference?: string }).reference ?? String(p);
          tryLoad(`${m}/${pid}/practice-set`, () =>
            getPracticeSet(TRACK, courseId, m, pid, undefined, locale),
          );
        }
        for (const c of getLessonChallenges(TRACK, courseId, m, lid)) {
          tryLoad(`${m}/${lid}/${c.id}/challenge`, () =>
            getChallenge(TRACK, courseId, m, lid, c.id, undefined, locale),
          );
        }
      }
      for (const pref of getCurriculumModule(TRACK, courseId, m).practices) {
        const pid = pref.reference;
        tryLoad(`${m}/${pid}/practice-set`, () =>
          getPracticeSet(TRACK, courseId, m, pid, undefined, locale),
        );
        for (const c of getPracticeChallenges(TRACK, courseId, m, pid)) {
          tryLoad(`${m}/${pid}/${c.id}/challenge`, () =>
            getPracticeChallenge(TRACK, courseId, m, pid, c.id, undefined, locale),
          );
        }
      }
    }
    if (localeFailures > 0) {
      console.log(`LOCALE: ${localeFailures} failures loading ${courseId} in ${locale}`);
      failed = true;
    } else {
      console.log(`LOCALE: ${locale} — ${loads} nodes load clean for ${courseId}`);
    }
  }
}

if (process.env.SWEEP_LINEAR === "1") {
  const tracks = COURSE_TRACKS.map((c) => c.track).filter((t, i, a) => a.indexOf(t) === i);
  for (const track of tracks) {
    console.log(`Linear path (${track}): ${getLinearLessons(track).length} lessons`);
  }
}
if (failed) process.exit(1);
