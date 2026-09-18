/**
 * Intermediate-course authoring library (Course 2).
 *
 * Writes EN json + mdx and VI sidecar json + mdx in one pass, so EN/VI stay
 * structurally synchronized by construction (spec §21). Call sites pass both
 * languages; the write helpers emit exactly the shapes the curriculum loaders
 * and zod schema expect.
 *
 * Escaping-safe convention for content strings: NO raw backticks and NO raw
 * "${" — use the T constant and string concat where needed.
 *
 * Used by the i2-*.mjs authoring scripts (run in module order).
 */
import { mkdirSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import path from "node:path";

export const T = String.fromCharCode(96);

const BASE = "src/content/tracks/web-development/courses/web-development-intermediate";
const SOLUTIONS_FILE = "scripts/content-authoring/i2-solutions.mjs";

export const MOD_DIR = (moduleId) => path.join(BASE, "modules", moduleId);
export const LESSONS = (moduleId) => path.join(MOD_DIR(moduleId), "lessons");
export const PRACTICES = (moduleId) => path.join(MOD_DIR(moduleId), "practices");
const P = (moduleId, setId) => path.join(PRACTICES(moduleId), setId, "challenges");

// ── module.json + module.vi.json ─────────────────────────────────────────
export function writeModule(moduleId, { title, summary, viTitle, viSummary, lessons, practices }) {
  mkdirSync(MOD_DIR(moduleId), { recursive: true });
  writeFileSync(
    path.join(MOD_DIR(moduleId), "module.json"),
    JSON.stringify(
      {
        id: moduleId,
        title,
        summary,
        lessons: lessons.map((l) => ({ reference: l })),
        practices: (practices ?? []).map((p) => ({ reference: p })),
      },
      null,
      2,
    ) + "\n",
  );
  if (viTitle) {
    writeFileSync(
      path.join(MOD_DIR(moduleId), "module.vi.json"),
      JSON.stringify({ title: viTitle, summary: viSummary }, null, 2) + "\n",
    );
  }
  console.log("module:", moduleId);
}

// ── lesson.json + lesson.vi.json + lesson.mdx + lesson.vi.mdx ────────────
export function writeLesson(moduleId, lesson, vi) {
  const dir = LESSONS(moduleId);
  mkdirSync(dir, { recursive: true });
  const base = {
    id: lesson.id,
    title: lesson.title,
    description: lesson.description,
    minutes: lesson.minutes,
    difficulty: lesson.difficulty,
    contentPath: "./" + lesson.id + ".mdx",
  };
  writeFileSync(path.join(dir, lesson.id + ".json"), JSON.stringify(base, null, 2) + "\n");
  writeFileSync(
    path.join(dir, lesson.id + ".vi.json"),
    JSON.stringify({ title: vi.title, description: vi.description }, null, 2) + "\n",
  );
  writeFileSync(path.join(dir, lesson.id + ".mdx"), lesson.mdx.trimStart() + "\n");
  writeFileSync(path.join(dir, lesson.id + ".vi.mdx"), vi.mdx.trimStart() + "\n");
  console.log("lesson:", moduleId + "/" + lesson.id);
}

// ── checkpoint: lesson + lessons/<id>/challenges/<challengeId>.json ──────
export function writeCheckpoint(moduleId, lesson, vi, challenge, viChallenge) {
  writeLesson(moduleId, lesson, vi);
  const chDir = path.join(LESSONS(moduleId), lesson.id, "challenges");
  mkdirSync(chDir, { recursive: true });
  writeFileSync(
    path.join(chDir, challenge.id + ".json"),
    JSON.stringify(challenge, null, 2) + "\n",
  );
  writeFileSync(
    path.join(chDir, challenge.id + ".vi.json"),
    JSON.stringify(viChallenge, null, 2) + "\n",
  );
  console.log("  checkpoint challenge:", challenge.id);
}

// ── practice set manifest + challenges (EN + VI) ─────────────────────────
export function writePracticeSet(moduleId, set, solutionPairs) {
  const { file, id, title, description, afterLesson, minutes, difficulty, challenges } = set;
  const dir = PRACTICES(moduleId);
  mkdirSync(path.join(dir, id, "challenges"), { recursive: true });
  writeFileSync(
    path.join(dir, file),
    JSON.stringify(
      {
        id,
        title,
        description,
        afterLesson,
        minutes,
        difficulty,
        challenges: challenges.map((c) => c.id),
      },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(
    path.join(dir, id + ".vi.json"),
    JSON.stringify({ title: set.viTitle, description: set.viDescription }, null, 2) + "\n",
  );
  for (const c of challenges) {
    const { id: cid, title: t, prompt, difficulty: diff, level, boilerplate, tests } = c;
    writeFileSync(
      path.join(P(moduleId, id), cid + ".json"),
      JSON.stringify(
        { id: cid, title: t, prompt, difficulty: diff, level, boilerplate, tests },
        null,
        2,
      ) + "\n",
    );
    const viC = c.vi;
    writeFileSync(
      path.join(P(moduleId, id), cid + ".vi.json"),
      JSON.stringify({ title: viC.title, prompt: viC.prompt, tests: viC.tests }, null, 2) + "\n",
    );
    console.log("  challenge:", moduleId + "/" + id + "/" + cid);
  }
  // Reference/wrong solutions → i2-solutions.mjs (consumed by the harness).
  if (solutionPairs) {
    if (!existsSync(SOLUTIONS_FILE)) {
      writeFileSync(
        SOLUTIONS_FILE,
        "/**\n * Intermediate-course challenge solutions. Appended by the i2-*.mjs\n * authoring scripts; imported by verify-challenges.mjs.\n */\nexport const R = {};\nexport const W = {};\n",
      );
    }
    for (const [cid, ref, wrong] of solutionPairs) {
      appendFileSync(
        SOLUTIONS_FILE,
        "R[" + JSON.stringify(cid) + "] = " + JSON.stringify(ref) + ";\n",
      );
      appendFileSync(
        SOLUTIONS_FILE,
        "W[" + JSON.stringify(cid) + "] = " + JSON.stringify(wrong) + ";\n",
      );
    }
  }
  console.log("practice set:", moduleId + "/" + id);
}
