import { z } from "zod";

/**
 * Curriculum content schemas (content-as-data, decision D-13).
 *
 * Content lives as version-controlled JSON + MDX under src/content/tracks/.
 * Every file is validated with these schemas when the curriculum is loaded;
 * invalid content throws at load time and therefore FAILS THE BUILD (CURR-04).
 */

export const SLUG_PATTERN = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const slugSchema = z
  .string()
  .regex(SLUG_PATTERN, "must be a lowercase slug (letters, digits, hyphens)");

const titleSchema = z.string().min(1).max(120);
const descriptionSchema = z.string().min(1).max(400);
const summarySchema = z.string().min(1).max(200);

/** Reference to a child entity by id — keeps ordering explicit. */
const referenceSchema = z.object({ reference: slugSchema });

export const difficultySchema = z.enum(["beginner", "intermediate", "advanced"]);

/**
 * One challenge test: an assertion snippet executed in the sandbox against
 * the student's code. `hint` is the educational failure message (CHAL-05) —
 * shown when the test fails, never a bare boolean.
 */
export const challengeTestSchema = z.object({
  name: z.string().min(1).max(120),
  /** JavaScript assertion code; has access to `code` (student source). */
  code: z.string().min(1),
  hint: z.string().min(1).max(400),
});

export const challengeSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  prompt: z.string().min(1).max(4000),
  difficulty: difficultySchema,
  /** Starter code pre-filled in the editor. */
  boilerplate: z.string().max(20_000),
  tests: z.array(challengeTestSchema).min(1, "challenge must define at least one test"),
});

export const lessonSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  description: descriptionSchema,
  /** Estimated reading/practice time in minutes (1–240). */
  minutes: z.number().int().min(1).max(240),
  difficulty: difficultySchema,
  /** Path to the lesson body (.mdx), relative to the lesson JSON file. */
  contentPath: z.string().min(1),
  /** Challenge ids attached to this lesson. Empty in Phase 2 (Phase 3 fills it). */
  challenges: z.array(slugSchema).max(50).default([]),
});

export const moduleSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  summary: summarySchema,
  lessons: z.array(referenceSchema).min(1, "module must contain at least one lesson"),
});

export const courseSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  description: descriptionSchema,
  modules: z.array(referenceSchema).min(1, "course must contain at least one module"),
});

export const trackSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  description: descriptionSchema,
  courses: z.array(referenceSchema).min(1, "track must contain at least one course"),
});

export type Track = z.infer<typeof trackSchema>;
export type Course = z.infer<typeof courseSchema>;
export type CurriculumModule = z.infer<typeof moduleSchema>;
export type Lesson = z.infer<typeof lessonSchema>;
export type Challenge = z.infer<typeof challengeSchema>;
export type ChallengeTest = z.infer<typeof challengeTestSchema>;
export type Difficulty = z.infer<typeof difficultySchema>;

/** A lesson joined with its resolved position in the track. */
export interface ResolvedLesson extends Lesson {
  trackId: string;
  courseId: string;
  moduleId: string;
  /** Zero-based position in the track's linear lesson order. */
  linearIndex: number;
}

/** A challenge joined with its fully-resolved curriculum location. */
export interface ResolvedChallenge extends Challenge {
  trackId: string;
  courseId: string;
  moduleId: string;
  lessonId: string;
}
