/**
 * MDX compile check scoped to the python-advanced course (EN + VI lessons).
 * Run: node --experimental-strip-types scripts/content-authoring/check-mdx-pa.mts
 */
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { compile } from "@mdx-js/mdx";
import remarkGfm from "remark-gfm";

const BASE = "src/content/tracks/python/courses/python-advanced/modules";
const files: string[] = [];
for (const mod of readdirSync(BASE)) {
  const lp = path.join(BASE, mod, "lessons");
  for (const f of readdirSync(lp)) {
    if (f.endsWith(".mdx")) files.push(path.join(lp, f));
  }
}

let bad = 0;
for (const f of files) {
  try {
    await compile(readFileSync(f, "utf8"), { remarkPlugins: [remarkGfm] });
  } catch (e) {
    bad++;
    console.log("FAIL", f, "\n  ", (e as Error).message.split("\n")[0]);
  }
}
console.log(`MDX: ${files.length - bad}/${files.length} compile clean (python-advanced)`);
if (bad > 0) process.exit(1);
