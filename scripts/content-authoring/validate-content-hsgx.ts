/**
 * Content validation for the HSG Intensive course (hsg-intensive) only.
 *
 * Mirrors validate-content.ts but loads through a scoped curriculum root
 * (a temp dir with a track.json copy stripped to this one course and a real
 * `courses` dir containing ONLY a deep copy of hsg-intensive) so that
 * in-flight, broken state from OTHER agents' courses in the hsg track never
 * blocks this QA pass. Every check runs through the real public loaders
 * (schema + VI overlays) in BOTH locales. Structural EN/VI sync is checked
 * on the real disk tree for this course only.
 *
 * Run: npx tsx scripts/content-authoring/validate-content-hsgx.ts
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
import { mkdtempSync, mkdirSync, cpSync, readFileSync, readdirSync, existsSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const TRACK = "hsg";
const COURSE = "hsg-intensive";
const REAL_COURSE_DIR = path.resolve("src/content/tracks", TRACK, "courses", COURSE);

// Scoped root: <tmp>/hsg/{track.json stripped to one course, courses/hsg-intensive copy}.
// (loadCurriculum treats the root as the tracks dir and SKIPS symlinked track
// dirs; a symlinked `courses` dir would drag in OTHER agents' hsg courses —
// hsg-mastery is in-flight from another agent — so: real `courses` dir with
// ONLY this course deep-copied into it.)
const root = mkdtempSync(path.join(tmpdir(), "hsgx-validate-"));
const trackDir = path.join(root, TRACK);
mkdirSync(trackDir);
const trackJson = JSON.parse(readFileSync(path.resolve("src/content/tracks", TRACK, "track.json"), "utf8")) as {
  courses: { reference: string }[];
};
trackJson.courses = trackJson.courses.filter((c) => c.reference === COURSE);
writeFileSync(path.join(trackDir, "track.json"), JSON.stringify(trackJson, null, 2));
mkdirSync(path.join(trackDir, "courses"));
cpSync(REAL_COURSE_DIR, path.join(trackDir, "courses", COURSE), { recursive: true });

let failed = false;
const fail = (msg: string) => {
  console.log(`  FAIL ${msg}`);
  failed = true;
};

try {
  const course = getCourse(TRACK, COURSE, root);
  console.log(`=== ${COURSE} ===`);
  console.log(`modules: ${course.modules.length}, title: ${course.title}`);

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

  // ── EN/VI structural synchronization (on the real tree, this course only) ─
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
  const walkJsonPairs = (dir: string) => {
    for (const f of readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, f.name);
      if (f.isDirectory()) {
        walkJsonPairs(full);
      } else if (f.name.endsWith(".json") && !f.name.endsWith(".vi.json")) {
        checkPair(full, full.replace(".json", ".vi.json"), path.relative(REAL_COURSE_DIR, full));
      }
    }
  };
  walkJsonPairs(REAL_COURSE_DIR);

  if (viMismatches > 0) {
    console.log(`SYNC: ${viMismatches} EN/VI structural mismatches in ${COURSE}`);
    failed = true;
  } else {
    console.log(`SYNC: EN/VI structures match for ${COURSE}`);
  }

  // ── Locale sweep: every node must load through the schema-validating ────
  // loaders in BOTH locales (structural file sync alone cannot catch a VI
  // overlay that fails schema validation, which only surfaces as a 404).
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
    if (locale === "vi" && loads < 140) fail(`vi locale loaded only ${loads} nodes`);
    console.log(`LOCALE: ${locale} — ${loads} nodes load clean`);
  }
} catch (e) {
  fail(`course load: ${e instanceof Error ? e.stack : e}`);
} finally {
  rmSync(root, { recursive: true, force: true });
}

if (failed) process.exit(1);
