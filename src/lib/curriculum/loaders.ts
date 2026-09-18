import { existsSync, readFileSync, readdirSync } from "node:fs";
import path from "node:path";

import {
  challengeSchema,
  courseSchema,
  lessonSchema,
  moduleSchema,
  practiceSetSchema,
  trackSchema,
  type Challenge,
  type Course,
  type CurriculumModule,
  type Lesson,
  type ResolvedChallenge,
  type ResolvedLesson,
  type ResolvedPracticeSet,
  type PracticeSet,
  type Track,
} from "./schema";

/**
 * Curriculum loaders (content-as-data). All files are parsed + validated on
 * load; cross-references and content paths are checked ONCE here — so invalid
 * content throws at build time (CURR-04), never silently at request time.
 *
 * Loaders accept an injectable root for tests (default src/content/tracks).
 */

export class CurriculumNotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CurriculumNotFoundError";
  }
}

import { DEFAULT_LOCALE, type Locale } from "@/lib/i18n/config";

function loadJson(filePath: string): unknown {
  try {
    return JSON.parse(readFileSync(filePath, "utf8"));
  } catch (error) {
    throw new Error(
      `Invalid curriculum content at ${filePath}: not parseable JSON (${(error as Error).message})`,
    );
  }
}

function parseOrThrow<T>(
  schema: { parse: (data: unknown) => T },
  data: unknown,
  filePath: string,
): T {
  try {
    return schema.parse(data);
  } catch (error) {
    const issues =
      error && typeof error === "object" && "issues" in error
        ? (error as { issues: { path: (string | number | symbol)[]; message: string }[] }).issues
            .map((i) => `${i.path.map(String).join(".") || "(root)"}: ${i.message}`)
            .join("; ")
        : String(error);
    throw new Error(`Invalid curriculum content at ${filePath}: ${issues}`);
  }
}

interface LoadedLesson {
  lesson: Lesson;
  filePath: string;
  bodyPath: string;
  /** Vietnamese body sidecar path when a `<lessonId>.vi.mdx` exists. */
  viBodyPath: string;
  challenges: Map<string, LoadedChallenge>;
}

interface LoadedPractice {
  practiceSet: PracticeSet;
  filePath: string;
  challenges: Map<string, LoadedChallenge>;
}

interface LoadedChallenge {
  challenge: Challenge;
  filePath: string;
}

interface LoadedCurriculum {
  tracks: Map<string, LoadedTrack>;
  /** Linear lesson order per track id (flattened across courses/modules). */
  linearLessons: Map<string, ResolvedLesson[]>;
}

interface LoadedTrack {
  track: Track;
  filePath: string;
  dir: string;
  courses: Map<string, LoadedCourse>;
}

interface LoadedCourse {
  course: Course;
  filePath: string;
  dir: string;
  modules: Map<string, LoadedModule>;
}

interface LoadedModule {
  module: CurriculumModule;
  filePath: string;
  dir: string;
  lessons: Map<string, LoadedLesson>;
  practices: Map<string, LoadedPractice>;
  /** Practice ids in declared order. */
  practiceOrder: string[];
}

/**
 * Read a Vietnamese translation sidecar (`<name>.vi.json` beside `<name>.json`).
 * Sidecars contain ONLY learner-facing text (titles, descriptions, prompts,
 * hints) — structural fields (ids, references, test code, boilerplate) always
 * come from the English source of truth. Missing sidecar → English fallback.
 */
function readViOverlay(filePath: string): Record<string, unknown> {
  const overlayPath = filePath.replace(/\.json$/, ".vi.json");
  if (!existsSync(overlayPath)) return {};
  const overlay = loadJson(overlayPath);
  return overlay && typeof overlay === "object" ? (overlay as Record<string, unknown>) : {};
}

/** Fields a simple content sidecar may override. */
const SIMPLE_TEXT_FIELDS = new Set(["title", "description", "summary", "audience"]);

/** Shallow-overlay merge for track/course/module/lesson/practice files. */
function overlaySimple<T>(
  schema: { parse: (data: unknown) => T },
  base: T,
  filePath: string,
  locale: Locale,
): T {
  if (locale === DEFAULT_LOCALE) return base;
  const vi = readViOverlay(filePath);
  const picked: Record<string, unknown> = {};
  for (const key of SIMPLE_TEXT_FIELDS) if (key in vi) picked[key] = vi[key];
  if (Array.isArray(vi.outcomes)) picked.outcomes = vi.outcomes;
  if (Object.keys(picked).length === 0) return base;
  return parseOrThrow(schema, { ...base, ...picked }, `${filePath} (vi overlay)`);
}

/**
 * Challenge overlay: title + prompt directly; per-test `name`/`hint` merged BY
 * INDEX onto the base tests. Test `code` (the graded logic) is never taken
 * from a sidecar — translations must never touch grading semantics.
 */
function overlayChallenge(
  base: Challenge,
  filePath: string,
  locale: Locale,
): Challenge {
  if (locale === DEFAULT_LOCALE) return base;
  const vi = readViOverlay(filePath) as {
    title?: unknown;
    prompt?: unknown;
    tests?: unknown;
  };
  const picked: Record<string, unknown> = {};
  if (typeof vi.title === "string") picked.title = vi.title;
  if (typeof vi.prompt === "string") picked.prompt = vi.prompt;
  if (Array.isArray(vi.tests)) {
    const viTests = vi.tests as unknown[];
    picked.tests = base.tests.map((test, i) => {
      const viTest = viTests[i];
      if (!viTest || typeof viTest !== "object") return test;
      const t = viTest as Record<string, unknown>;
      return {
        ...test,
        ...(typeof t.name === "string" ? { name: t.name } : {}),
        ...(typeof t.hint === "string" ? { hint: t.hint } : {}),
      };
    });
  }
  if (Object.keys(picked).length === 0) return base;
  return parseOrThrow(challengeSchema, { ...base, ...picked }, `${filePath} (vi overlay)`);
}

function loadChallenge(
  challengesDir: string,
  challengeId: string,
  lessonFilePath: string,
  locale: Locale,
): LoadedChallenge {
  const filePath = path.join(challengesDir, `${challengeId}.json`);
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content at ${lessonFilePath}: challenge reference "${challengeId}" has no file at ${filePath}`,
    );
  }
  const base = parseOrThrow(challengeSchema, loadJson(filePath), filePath);
  return {
    challenge: overlayChallenge(base, filePath, locale),
    filePath,
  };
}

/**
 * Practice sets live at modules/<moduleId>/practices/<practiceId>.json with
 * their challenges at practices/<practiceId>/challenges/<challengeId>.json —
 * the same challenge file format as lessons.
 */
function loadPracticeSet(practicesDir: string, practiceId: string, locale: Locale): LoadedPractice {
  const filePath = path.join(practicesDir, `${practiceId}.json`);
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: practice reference "${practiceId}" has no file at ${filePath}`,
    );
  }
  const practiceSet = overlaySimple(
    practiceSetSchema,
    parseOrThrow(practiceSetSchema, loadJson(filePath), filePath),
    filePath,
    locale,
  );
  const challengesDir = path.join(practicesDir, practiceId, "challenges");
  const challenges = new Map<string, LoadedChallenge>();
  for (const challengeId of practiceSet.challenges) {
    if (challenges.has(challengeId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate challenge reference "${challengeId}"`,
      );
    }
    challenges.set(challengeId, loadChallenge(challengesDir, challengeId, filePath, locale));
  }
  return { practiceSet, filePath, challenges };
}

function loadLesson(
  lessonsDir: string,
  lessonId: string,
  moduleDir: string,
  locale: Locale,
): LoadedLesson {
  const filePath = path.join(lessonsDir, `${lessonId}.json`);
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: lesson reference "${lessonId}" has no file at ${filePath}`,
    );
  }
  const lesson = overlaySimple(
    lessonSchema,
    parseOrThrow(lessonSchema, loadJson(filePath), filePath),
    filePath,
    locale,
  );
  const bodyPath = path.resolve(path.dirname(filePath), lesson.contentPath);
  if (!existsSync(bodyPath)) {
    throw new Error(
      `Invalid curriculum content at ${filePath}: contentPath "${lesson.contentPath}" does not resolve to an existing file (expected ${bodyPath})`,
    );
  }
  // contentPath must stay inside the module's lesson directory.
  if (!bodyPath.startsWith(path.resolve(moduleDir))) {
    throw new Error(
      `Invalid curriculum content at ${filePath}: contentPath "${lesson.contentPath}" escapes the lesson directory`,
    );
  }
  // Legacy lesson-attached challenges (checkpoints): any challenge JSON in
  // …/lessons/<lessonId>/challenges/ belongs to this lesson. Regular lessons
  // have no challenges dir — all coding lives in practice sets (Course 1
  // revision phase 2).
  const challengesDir = path.join(path.dirname(filePath), lessonId, "challenges");
  const challenges = new Map<string, LoadedChallenge>();
  if (existsSync(challengesDir)) {
    // Sidecar translations (<id>.vi.json) are overlays, not challenges.
    const files = readdirSync(challengesDir).filter(
      (f) => f.endsWith(".json") && !f.endsWith(".vi.json"),
    );
    for (const file of files) {
      const challengeId = file.replace(/\.json$/, "");
      challenges.set(challengeId, loadChallenge(challengesDir, challengeId, filePath, locale));
    }
  }
  const viBodyPath = bodyPath.replace(/\.mdx$/, ".vi.mdx");
  return { lesson, filePath, bodyPath, viBodyPath, challenges };
}

function loadModule(modulesDir: string, moduleId: string, locale: Locale): LoadedModule {
  const dir = path.join(modulesDir, moduleId);
  const filePath = path.join(dir, "module.json");
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: module reference "${moduleId}" has no file at ${filePath}`,
    );
  }
  const moduleData = overlaySimple(
    moduleSchema,
    parseOrThrow(moduleSchema, loadJson(filePath), filePath),
    filePath,
    locale,
  );
  const lessonsDir = path.join(dir, "lessons");
  const lessons = new Map<string, LoadedLesson>();
  for (const ref of moduleData.lessons) {
    const lessonId = ref.reference;
    if (lessons.has(lessonId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate lesson reference "${lessonId}"`,
      );
    }
    lessons.set(lessonId, loadLesson(lessonsDir, lessonId, dir, locale));
  }
  // Practice sets (Course 1 revision): practices/<id>.json, declared in
  // module.json's top-level `practices` array.
  const practices = new Map<string, LoadedPractice>();
  const practiceOrder: string[] = [];
  const practicesDir = path.join(dir, "practices");
  const declaredPractices = moduleData.practices;
  for (const ref of declaredPractices) {
    const practiceId = ref.reference;
    if (practices.has(practiceId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate practice reference "${practiceId}"`,
      );
    }
    if (moduleData.lessons.some((l) => l.reference === practiceId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: id "${practiceId}" used by both a lesson and a practice`,
      );
    }
    practices.set(practiceId, loadPracticeSet(practicesDir, practiceId, locale));
    practiceOrder.push(practiceId);
  }
  // afterLesson anchors must point at lessons in the same module.
  for (const practiceId of practiceOrder) {
    const anchor = practices.get(practiceId)?.practiceSet.afterLesson;
    if (anchor && !lessons.has(anchor)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: practice "${practiceId}" afterLesson "${anchor}" is not a lesson in this module`,
      );
    }
  }
  return { module: moduleData, filePath, dir, lessons, practices, practiceOrder };
}

function loadCourse(coursesDir: string, courseId: string, locale: Locale): LoadedCourse {
  const dir = path.join(coursesDir, courseId);
  const filePath = path.join(dir, "course.json");
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: course reference "${courseId}" has no file at ${filePath}`,
    );
  }
  const course = overlaySimple(
    courseSchema,
    parseOrThrow(courseSchema, loadJson(filePath), filePath),
    filePath,
    locale,
  );
  const modulesDir = path.join(dir, "modules");
  const modules = new Map<string, LoadedModule>();
  for (const ref of course.modules) {
    const moduleId = ref.reference;
    if (modules.has(moduleId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate module reference "${moduleId}"`,
      );
    }
    modules.set(moduleId, loadModule(modulesDir, moduleId, locale));
  }
  return { course, filePath, dir, modules };
}

function loadTrack(trackDir: string, locale: Locale): LoadedTrack {
  const filePath = path.join(trackDir, "track.json");
  const track = overlaySimple(
    trackSchema,
    parseOrThrow(trackSchema, loadJson(filePath), filePath),
    filePath,
    locale,
  );
  const coursesDir = path.join(trackDir, "courses");
  const courses = new Map<string, LoadedCourse>();
  for (const ref of track.courses) {
    const courseId = ref.reference;
    if (courses.has(courseId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate course reference "${courseId}"`,
      );
    }
    try {
      courses.set(courseId, loadCourse(coursesDir, courseId, locale));
    } catch (error) {
      // A deliberately empty course shell (parseable course.json with an
      // explicit empty modules list) means a content author has scaffolded
      // the course but not populated it yet — this repo is authored by
      // several agents concurrently. Failing the WHOLE curriculum for it
      // took down every page, the sitemap, and the challenge run API
      // (learner report 2026-09-13: browser "TypeError: Failed to fetch").
      // Exclude the shell; everything else still throws loudly so real
      // content bugs are never silently swallowed.
      if (isAuthoringShell(path.join(coursesDir, courseId, "course.json"))) {
        continue;
      }
      throw error;
    }
  }
  return { track, filePath, dir: trackDir, courses };
}

/**
 * Deliberately empty course shell: parseable course.json with an explicit
 * empty `modules` array — the convention content agents use to scaffold a
 * course in progress. See the loadTrack catch for why shells are skipped
 * instead of fatal. Missing/unparseable files are NOT shells — those stay
 * loud so a typo'd filename is still caught.
 */
function isAuthoringShell(courseJsonPath: string): boolean {
  if (!existsSync(courseJsonPath)) return false;
  try {
    const raw = JSON.parse(readFileSync(courseJsonPath, "utf8")) as {
      modules?: unknown;
    };
    return Array.isArray(raw.modules) && raw.modules.length === 0;
  } catch {
    return false;
  }
}

/** Global id uniqueness across the whole curriculum. */
function assertUniqueIds(curriculum: LoadedCurriculum): void {
  const seen = new Map<string, string>();
  const check = (id: string, kind: string, filePath: string) => {
    const prior = seen.get(id);
    if (prior) {
      throw new Error(
        `Invalid curriculum content: duplicate id "${id}" (${kind}) used in ${filePath} and ${prior}`,
      );
    }
    seen.set(id, filePath);
  };

  for (const loadedTrack of curriculum.tracks.values()) {
    check(loadedTrack.track.id, "track", loadedTrack.filePath);
    for (const loadedCourse of loadedTrack.courses.values()) {
      check(loadedCourse.course.id, "course", loadedCourse.filePath);
      for (const loadedModule of loadedCourse.modules.values()) {
        check(loadedModule.module.id, "module", loadedModule.filePath);
        for (const loadedLesson of loadedModule.lessons.values()) {
          check(loadedLesson.lesson.id, "lesson", loadedLesson.filePath);
          for (const loadedChallenge of loadedLesson.challenges.values()) {
            check(loadedChallenge.challenge.id, "challenge", loadedChallenge.filePath);
          }
        }
        for (const loadedPractice of loadedModule.practices.values()) {
          check(loadedPractice.practiceSet.id, "practice", loadedPractice.filePath);
          for (const loadedChallenge of loadedPractice.challenges.values()) {
            check(loadedChallenge.challenge.id, "challenge", loadedChallenge.filePath);
          }
        }
      }
    }
  }
}

function buildLinearOrder(curriculum: LoadedCurriculum): void {
  curriculum.linearLessons = new Map();
  for (const loadedTrack of curriculum.tracks.values()) {
    const linear: ResolvedLesson[] = [];
    for (const loadedCourse of loadedTrack.courses.values()) {
      for (const loadedModule of loadedCourse.modules.values()) {
        for (const loadedLesson of loadedModule.lessons.values()) {
          linear.push({
            ...loadedLesson.lesson,
            trackId: loadedTrack.track.id,
            courseId: loadedCourse.course.id,
            moduleId: loadedModule.module.id,
            linearIndex: linear.length,
          });
        }
      }
    }
    curriculum.linearLessons.set(loadedTrack.track.id, linear);
  }
}

function loadCurriculum(root: string, locale: Locale): LoadedCurriculum {
  const tracks = new Map<string, LoadedTrack>();
  if (!existsSync(root)) {
    return { tracks, linearLessons: new Map() };
  }
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const trackDir = path.join(root, entry.name);
    if (!existsSync(path.join(trackDir, "track.json"))) continue;
    const loaded = loadTrack(trackDir, locale);
    tracks.set(loaded.track.id, loaded);
  }
  const curriculum: LoadedCurriculum = { tracks, linearLessons: new Map() };
  assertUniqueIds(curriculum);
  buildLinearOrder(curriculum);
  return curriculum;
}

const DEFAULT_ROOT = path.join(process.cwd(), "src", "content", "tracks");

/** One fully-loaded (and overlaid) curriculum per locale — caches never mix locales. */
const defaultCurricula = new Map<Locale, LoadedCurriculum>();

function getCurriculum(root: string | undefined, locale: Locale): LoadedCurriculum {
  if (root) return loadCurriculum(root, locale);
  let cached = defaultCurricula.get(locale);
  if (!cached) {
    cached = loadCurriculum(DEFAULT_ROOT, locale);
    defaultCurricula.set(locale, cached);
  }
  return cached;
}

// ── Public accessors ──────────────────────────────────────────────────────

export function getTracks(root?: string, locale: Locale = DEFAULT_LOCALE): Track[] {
  return [...getCurriculum(root, locale).tracks.values()].map((t) => t.track);
}

export function getTrack(trackId: string, root?: string, locale: Locale = DEFAULT_LOCALE): Track {
  const loaded = getCurriculum(root, locale).tracks.get(trackId);
  if (!loaded) {
    throw new CurriculumNotFoundError(`Track not found: ${trackId}`);
  }
  return loaded.track;
}

export function getCourse(trackId: string, courseId: string, root?: string, locale: Locale = DEFAULT_LOCALE): Course {
  const course = getCurriculum(root, locale).tracks.get(trackId)?.courses.get(courseId)?.course;
  if (!course) {
    throw new CurriculumNotFoundError(`Course not found: ${courseId} (in track ${trackId})`);
  }
  return course;
}

/**
 * Loaded courses of a track, in manifest order. Unlike `getTrack` (raw
 * manifest references), this reflects loadTrack's authoring-shell exclusion:
 * a scaffolded course with an empty modules list is not returned, so
 * callers iterating courses never hit CurriculumNotFoundError for it.
 */
export function getLoadedCourses(
  trackId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): Course[] {
  const loaded = getCurriculum(root, locale).tracks.get(trackId);
  if (!loaded) {
    throw new CurriculumNotFoundError(`Track not found: ${trackId}`);
  }
  return [...loaded.courses.values()].map((c) => c.course);
}

export function getCurriculumModule(
  trackId: string,
  courseId: string,
  moduleId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): CurriculumModule {
  const moduleData = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)?.module;
  if (!moduleData) {
    throw new CurriculumNotFoundError(`Module not found: ${moduleId} (in ${trackId}/${courseId})`);
  }
  return moduleData;
}

export function getLesson(
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedLesson {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.lessons.get(lessonId);
  if (!loaded) {
    throw new CurriculumNotFoundError(
      `Lesson not found: ${lessonId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  const linear = getCurriculum(root, locale).linearLessons.get(trackId) ?? [];
  const resolved = linear.find(
    (l) => l.id === lessonId && l.moduleId === moduleId && l.courseId === courseId,
  );
  return resolved ?? { ...loaded.lesson, trackId, courseId, moduleId, linearIndex: -1 };
}

export function getLinearLessons(trackId: string, root?: string, locale: Locale = DEFAULT_LOCALE): ResolvedLesson[] {
  return getCurriculum(root, locale).linearLessons.get(trackId) ?? [];
}

export function getLinearNeighbors(
  trackId: string,
  lessonId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): { prev: ResolvedLesson | null; next: ResolvedLesson | null } {
  const linear = getLinearLessons(trackId, root, locale);
  const index = linear.findIndex((l) => l.id === lessonId);
  if (index === -1) return { prev: null, next: null };
  return {
    prev: index > 0 ? (linear[index - 1] ?? null) : null,
    next: index < linear.length - 1 ? (linear[index + 1] ?? null) : null,
  };
}

/**
 * All practice sets of a module, in declared (module.json) order.
 * Throws CurriculumNotFoundError when the module doesn't exist.
 */
export function getModulePractices(
  trackId: string,
  courseId: string,
  moduleId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedPracticeSet[] {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId);
  if (!loaded) {
    throw new CurriculumNotFoundError(`Module not found: ${moduleId} (in ${trackId}/${courseId})`);
  }
  return loaded.practiceOrder.map((id, index) => ({
    ...loaded.practices.get(id)!.practiceSet,
    trackId,
    courseId,
    moduleId,
    practiceIndex: index,
  }));
}

/** One practice set with its full curriculum location. */
export function getPracticeSet(
  trackId: string,
  courseId: string,
  moduleId: string,
  practiceId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedPracticeSet {
  const practices = getModulePractices(trackId, courseId, moduleId, root, locale);
  const practiceSet = practices.find((p) => p.id === practiceId);
  if (!practiceSet) {
    throw new CurriculumNotFoundError(
      `Practice set not found: ${practiceId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  return practiceSet;
}

/**
 * All challenges of a practice set, in declared order.
 * Throws CurriculumNotFoundError when the practice set doesn't exist.
 */
export function getPracticeChallenges(
  trackId: string,
  courseId: string,
  moduleId: string,
  practiceId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): Challenge[] {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.practices.get(practiceId);
  if (!loaded) {
    throw new CurriculumNotFoundError(
      `Practice set not found: ${practiceId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  return loaded.practiceSet.challenges.map((id) => {
    const challenge = loaded.challenges.get(id);
    if (!challenge) {
      throw new CurriculumNotFoundError(
        `Challenge not found: ${id} (on practice set ${practiceId})`,
      );
    }
    return challenge.challenge;
  });
}

/** One challenge within a practice set, with its full curriculum location. */
export function getPracticeChallenge(
  trackId: string,
  courseId: string,
  moduleId: string,
  practiceId: string,
  challengeId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedChallenge {
  const practiceSet = getPracticeSet(trackId, courseId, moduleId, practiceId, root, locale);
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.practices.get(practiceId);
  const challenge = loaded?.challenges.get(challengeId);
  if (!loaded || !challenge) {
    throw new CurriculumNotFoundError(
      `Challenge not found: ${challengeId} (on practice set ${practiceId})`,
    );
  }
  return {
    ...challenge.challenge,
    trackId: practiceSet.trackId,
    courseId: practiceSet.courseId,
    moduleId: practiceSet.moduleId,
    lessonId: practiceSet.id,
  };
}

/**
 * The module's interleaved Learn → Practice flow: lessons in order with each
 * practice set inserted after its `afterLesson` anchor (unanchored sets at
 * the end of the module).
 */
export type ModuleFlowStep =
  | { kind: "lesson"; lesson: ResolvedLesson }
  | { kind: "practice"; practiceSet: ResolvedPracticeSet };

export function getModuleFlow(
  trackId: string,
  courseId: string,
  moduleId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ModuleFlowStep[] {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId);
  if (!loaded) {
    throw new CurriculumNotFoundError(`Module not found: ${moduleId} (in ${trackId}/${courseId})`);
  }
  const practices = getModulePractices(trackId, courseId, moduleId, root, locale);
  const steps: ModuleFlowStep[] = [];
  for (const lessonRef of loaded.module.lessons) {
    const lesson = loaded.lessons.get(lessonRef.reference);
    if (!lesson) continue;
    steps.push({
      kind: "lesson",
      lesson: {
        ...lesson.lesson,
        trackId,
        courseId,
        moduleId,
        linearIndex: -1,
      },
    });
    const anchored = practices.filter((p) => p.afterLesson === lessonRef.reference);
    for (const practiceSet of anchored) {
      steps.push({ kind: "practice", practiceSet });
    }
  }
  for (const practiceSet of practices.filter((p) => !p.afterLesson)) {
    steps.push({ kind: "practice", practiceSet });
  }
  return steps;
}

/**
 * Legacy challenges attached to a lesson (checkpoints only, Course 1
 * revision phase 2). Returns [] for regular lessons — their coding lives
 * in practice sets. Kept for back-compat with achievements/dashboard.
 */
export function getLessonChallenges(
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): Challenge[] {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.lessons.get(lessonId);
  if (!loaded) {
    throw new CurriculumNotFoundError(
      `Lesson not found: ${lessonId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  return [...loaded.challenges.values()].map((c) => c.challenge);
}

/**
 * All practice sets anchored to a lesson, in module-declared order.
 * Used by the lesson page, course page, and progress recording to know
 * every challenge a lesson's completion depends on.
 */
export function getLessonPractices(
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedPracticeSet[] {
  return getModulePractices(trackId, courseId, moduleId, root, locale).filter(
    (p) => p.afterLesson === lessonId,
  );
}

/**
 * Find the practice set that owns a challenge id (Course 1 revision phase 2:
 * challenges migrated from lessons into practice sets). Returns null when the
 * challenge is lesson-attached (checkpoint) or doesn't exist.
 */
export function findPracticeForChallenge(
  trackId: string,
  courseId: string,
  moduleId: string,
  challengeId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedPracticeSet | null {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId);
  if (!loaded) return null;
  for (const practiceId of loaded.practiceOrder) {
    const practice = loaded.practices.get(practiceId);
    if (practice?.challenges.has(challengeId)) {
      return {
        ...practice.practiceSet,
        trackId,
        courseId,
        moduleId,
        practiceIndex: loaded.practiceOrder.indexOf(practiceId),
      };
    }
  }
  return null;
}

/** One challenge with its full curriculum location. */
export function getChallenge(
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
  challengeId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): ResolvedChallenge {
  const lesson = getLesson(trackId, courseId, moduleId, lessonId, root, locale);
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.lessons.get(lessonId);
  const challenge = loaded?.challenges.get(challengeId);
  if (!loaded || !challenge) {
    throw new CurriculumNotFoundError(
      `Challenge not found: ${challengeId} (on lesson ${lessonId} in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  return {
    ...challenge.challenge,
    trackId: lesson.trackId,
    courseId: lesson.courseId,
    moduleId: lesson.moduleId,
    lessonId: lesson.id,
  };
}

/** Read a lesson body (MDX source) — used by the renderer via mdx-map. */
export function readLessonBody(
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
  root?: string,
  locale: Locale = DEFAULT_LOCALE,
): string {
  const loaded = getCurriculum(root, locale)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.lessons.get(lessonId);
  if (!loaded) {
    throw new CurriculumNotFoundError(
      `Lesson not found: ${lessonId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  // Vietnamese body sidecar when it exists; English fallback otherwise.
  const bodyPath = locale === DEFAULT_LOCALE ? loaded.bodyPath : loaded.viBodyPath;
  if (locale === DEFAULT_LOCALE || existsSync(bodyPath)) {
    return readFileSync(bodyPath, "utf8");
  }
  return readFileSync(loaded.bodyPath, "utf8");
}
