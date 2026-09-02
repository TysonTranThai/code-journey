import { existsSync, readFileSync, readdirSync } from "node:fs";
import path from "node:path";

import {
  courseSchema,
  lessonSchema,
  moduleSchema,
  trackSchema,
  type Course,
  type CurriculumModule,
  type Lesson,
  type ResolvedLesson,
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
}

function loadLesson(lessonsDir: string, lessonId: string, moduleDir: string): LoadedLesson {
  const filePath = path.join(lessonsDir, `${lessonId}.json`);
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: lesson reference "${lessonId}" has no file at ${filePath}`,
    );
  }
  const lesson = parseOrThrow(lessonSchema, loadJson(filePath), filePath);
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
  return { lesson, filePath, bodyPath };
}

function loadModule(modulesDir: string, moduleId: string): LoadedModule {
  const dir = path.join(modulesDir, moduleId);
  const filePath = path.join(dir, "module.json");
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: module reference "${moduleId}" has no file at ${filePath}`,
    );
  }
  const moduleData = parseOrThrow(moduleSchema, loadJson(filePath), filePath);
  const lessonsDir = path.join(dir, "lessons");
  const lessons = new Map<string, LoadedLesson>();
  for (const ref of moduleData.lessons) {
    const lessonId = ref.reference;
    if (lessons.has(lessonId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate lesson reference "${lessonId}"`,
      );
    }
    lessons.set(lessonId, loadLesson(lessonsDir, lessonId, dir));
  }
  return { module: moduleData, filePath, dir, lessons };
}

function loadCourse(coursesDir: string, courseId: string): LoadedCourse {
  const dir = path.join(coursesDir, courseId);
  const filePath = path.join(dir, "course.json");
  if (!existsSync(filePath)) {
    throw new Error(
      `Invalid curriculum content: course reference "${courseId}" has no file at ${filePath}`,
    );
  }
  const course = parseOrThrow(courseSchema, loadJson(filePath), filePath);
  const modulesDir = path.join(dir, "modules");
  const modules = new Map<string, LoadedModule>();
  for (const ref of course.modules) {
    const moduleId = ref.reference;
    if (modules.has(moduleId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate module reference "${moduleId}"`,
      );
    }
    modules.set(moduleId, loadModule(modulesDir, moduleId));
  }
  return { course, filePath, dir, modules };
}

function loadTrack(trackDir: string): LoadedTrack {
  const filePath = path.join(trackDir, "track.json");
  const track = parseOrThrow(trackSchema, loadJson(filePath), filePath);
  const coursesDir = path.join(trackDir, "courses");
  const courses = new Map<string, LoadedCourse>();
  for (const ref of track.courses) {
    const courseId = ref.reference;
    if (courses.has(courseId)) {
      throw new Error(
        `Invalid curriculum content at ${filePath}: duplicate course reference "${courseId}"`,
      );
    }
    courses.set(courseId, loadCourse(coursesDir, courseId));
  }
  return { track, filePath, dir: trackDir, courses };
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

function loadCurriculum(root: string): LoadedCurriculum {
  const tracks = new Map<string, LoadedTrack>();
  if (!existsSync(root)) {
    return { tracks, linearLessons: new Map() };
  }
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const trackDir = path.join(root, entry.name);
    if (!existsSync(path.join(trackDir, "track.json"))) continue;
    const loaded = loadTrack(trackDir);
    tracks.set(loaded.track.id, loaded);
  }
  const curriculum: LoadedCurriculum = { tracks, linearLessons: new Map() };
  assertUniqueIds(curriculum);
  buildLinearOrder(curriculum);
  return curriculum;
}

const DEFAULT_ROOT = path.join(process.cwd(), "src", "content", "tracks");

let defaultCurriculum: LoadedCurriculum | undefined;

function getCurriculum(root?: string): LoadedCurriculum {
  if (root) return loadCurriculum(root);
  defaultCurriculum ??= loadCurriculum(DEFAULT_ROOT);
  return defaultCurriculum;
}

// ── Public accessors ──────────────────────────────────────────────────────

export function getTracks(root?: string): Track[] {
  return [...getCurriculum(root).tracks.values()].map((t) => t.track);
}

export function getTrack(trackId: string, root?: string): Track {
  const loaded = getCurriculum(root).tracks.get(trackId);
  if (!loaded) {
    throw new CurriculumNotFoundError(`Track not found: ${trackId}`);
  }
  return loaded.track;
}

export function getCourse(trackId: string, courseId: string, root?: string): Course {
  const course = getCurriculum(root).tracks.get(trackId)?.courses.get(courseId)?.course;
  if (!course) {
    throw new CurriculumNotFoundError(`Course not found: ${courseId} (in track ${trackId})`);
  }
  return course;
}

export function getCurriculumModule(
  trackId: string,
  courseId: string,
  moduleId: string,
  root?: string,
): CurriculumModule {
  const moduleData = getCurriculum(root)
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
): ResolvedLesson {
  const loaded = getCurriculum(root)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.lessons.get(lessonId);
  if (!loaded) {
    throw new CurriculumNotFoundError(
      `Lesson not found: ${lessonId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  const linear = getCurriculum(root).linearLessons.get(trackId) ?? [];
  const resolved = linear.find(
    (l) => l.id === lessonId && l.moduleId === moduleId && l.courseId === courseId,
  );
  return resolved ?? { ...loaded.lesson, trackId, courseId, moduleId, linearIndex: -1 };
}

export function getLinearLessons(trackId: string, root?: string): ResolvedLesson[] {
  return getCurriculum(root).linearLessons.get(trackId) ?? [];
}

export function getLinearNeighbors(
  trackId: string,
  lessonId: string,
  root?: string,
): { prev: ResolvedLesson | null; next: ResolvedLesson | null } {
  const linear = getLinearLessons(trackId, root);
  const index = linear.findIndex((l) => l.id === lessonId);
  if (index === -1) return { prev: null, next: null };
  return {
    prev: index > 0 ? (linear[index - 1] ?? null) : null,
    next: index < linear.length - 1 ? (linear[index + 1] ?? null) : null,
  };
}

/** Read a lesson body (MDX source) — used by the renderer via mdx-map. */
export function readLessonBody(
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
  root?: string,
): string {
  const loaded = getCurriculum(root)
    .tracks.get(trackId)
    ?.courses.get(courseId)
    ?.modules.get(moduleId)
    ?.lessons.get(lessonId);
  if (!loaded) {
    throw new CurriculumNotFoundError(
      `Lesson not found: ${lessonId} (in ${trackId}/${courseId}/${moduleId})`,
    );
  }
  return readFileSync(loaded.bodyPath, "utf8");
}
