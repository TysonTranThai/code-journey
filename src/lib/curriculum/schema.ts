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

/**
 * Deliberate-practice levels (Course 1 revision). A practice set orders its
 * challenges so learners climb from imitation to real-world builds instead
 * of repeating one difficulty forever.
 */
export const practiceLevelSchema = z.enum([
  "imitation",
  "guided",
  "independent",
  "combination",
  "real-world",
  "debugging",
  "mini-build",
]);
export type PracticeLevel = z.infer<typeof practiceLevelSchema>;

/** Learner-facing label for a deliberate-practice level. */
export const PRACTICE_LEVEL_LABELS: Record<PracticeLevel, string> = {
  imitation: "Imitation",
  guided: "Guided",
  independent: "Independent",
  combination: "Combination",
  "real-world": "Real-world",
  debugging: "Debugging",
  "mini-build": "Mini build",
};

export const challengeSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  prompt: z.union([
    z.string().min(1).max(4000),
    z.array(z.string()).transform((lines) => lines.join("\n")),
  ]),
  difficulty: difficultySchema,
  /**
   * Deliberate-practice level (Course 1 revision). Required on practice-set
   * challenges so a set visibly climbs imitation → mini-build; legacy lesson
   * challenges (checkpoints) may omit it.
   */
  level: practiceLevelSchema.optional(),
  /**
   * Language the sandbox executes (Python, C++, Java, C, and C# tracks).
   * Defaults to "javascript" so every existing web-development challenge is
   * unchanged.
   */
  language: z.enum(["javascript", "python", "cpp", "java", "c", "csharp"]).default("javascript"),
  /** Starter code pre-filled in the editor. */
  boilerplate: z.string().max(20_000),
  tests: z.array(challengeTestSchema).min(1, "challenge must define at least one test"),
});

export const practiceSetSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  /** What concept this set drills, in learner-facing language. */
  description: descriptionSchema,
  /** The lesson this practice follows in the module flow. */
  afterLesson: slugSchema.optional(),
  /** Estimated hands-on coding time in minutes (1–240). */
  minutes: z.number().int().min(1).max(240),
  difficulty: difficultySchema,
  challenges: z.array(slugSchema).min(1, "practice set must contain at least one challenge"),
});

export const lessonSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  description: descriptionSchema,
  /** Estimated reading time in minutes (1–240). */
  minutes: z.number().int().min(1).max(240),
  difficulty: difficultySchema,
  /** Path to the lesson body (.mdx), relative to the lesson JSON file. */
  contentPath: z.string().min(1),
});

export const moduleSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  summary: summarySchema,
  lessons: z.array(referenceSchema).min(1, "module must contain at least one lesson"),
  /** Practice sets in this module (Course 1 revision) — interleaved after lessons. */
  practices: z.array(referenceSchema).default([]),
});

export const courseSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  description: descriptionSchema,
  modules: z.array(referenceSchema).min(1, "course must contain at least one module"),
  /** Who this course is for, in learner-facing language (course landing). */
  audience: z.string().min(1).max(400),
  /** What a learner can do after finishing (course landing). */
  outcomes: z.array(z.string().min(1).max(200)).min(1, "course must list learning outcomes"),
  /**
   * Course ids that must be completed first (Course 2+). Empty for the
   * entry course. The course page renders a prerequisite callout when set.
   */
  prerequisites: z.array(slugSchema).default([]),
});

export const trackSchema = z.object({
  id: slugSchema,
  title: titleSchema,
  description: descriptionSchema,
  image: z.string().startsWith("/").optional(),
  courses: z.array(referenceSchema).min(1, "track must contain at least one course"),
});

export type Challenge = z.infer<typeof challengeSchema>;
export type ChallengeTest = z.infer<typeof challengeTestSchema>;
export type Lesson = z.infer<typeof lessonSchema>;
export type PracticeSet = z.infer<typeof practiceSetSchema>;
export type Course = z.infer<typeof courseSchema>;
export type CurriculumModule = z.infer<typeof moduleSchema>;
export type Track = z.infer<typeof trackSchema>;

/** A challenge resolved to its curriculum location. */
export interface ResolvedChallenge extends Challenge {
  trackId: string;
  courseId: string;
  moduleId: string;
  lessonId: string;
}

/** A practice set resolved to its curriculum location. */
export interface ResolvedPracticeSet extends PracticeSet {
  trackId: string;
  courseId: string;
  moduleId: string;
  practiceIndex: number;
}

/** A lesson resolved to its curriculum location. */
export interface ResolvedLesson extends Lesson {
  trackId: string;
  courseId: string;
  moduleId: string;
  linearIndex: number;
}
