import { readFileSync } from "node:fs";
import path from "node:path";

import { z } from "zod";

/**
 * Achievement definitions as content-as-data (04-CONTEXT D-02): validated
 * with zod at load; lives in git like the curriculum, no DB seeding.
 */
export const achievementDefSchema = z.object({
  id: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/, "must be a lowercase slug"),
  title: z.string().min(1).max(120),
  description: z.string().min(1).max(400),
  icon: z.string().min(1).max(8),
});

export type AchievementDef = z.infer<typeof achievementDefSchema>;

let cachedDefsEn: AchievementDef[] | undefined;
let cachedDefsVi: AchievementDef[] | undefined;

function loadDefs(filename: string): AchievementDef[] {
  const filePath = path.join(process.cwd(), "src", "content", filename);
  const raw: unknown = JSON.parse(readFileSync(filePath, "utf8"));
  const parsed = z.array(achievementDefSchema).parse(raw);
  const seen = new Set<string>();
  for (const def of parsed) {
    if (seen.has(def.id)) {
      throw new Error(`Duplicate achievement id: ${def.id}`);
    }
    seen.add(def.id);
  }
  return parsed;
}

export function getAchievementDefs(locale?: string): AchievementDef[] {
  if (locale === "vi") {
    cachedDefsVi ??= loadDefs("achievements.vi.json");
    return cachedDefsVi;
  }
  cachedDefsEn ??= loadDefs("achievements.json");
  return cachedDefsEn;
}

export function getAchievementDef(id: string, locale?: string): AchievementDef | undefined {
  return getAchievementDefs(locale).find((d) => d.id === id);
}
