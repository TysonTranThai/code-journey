import path from "node:path";

import IntroductionToHtml from "@/content/tracks/web-development/courses/web-development-foundations/modules/html-foundations/lessons/introduction-to-html.mdx";
import HtmlAttributes from "@/content/tracks/web-development/courses/web-development-foundations/modules/html-foundations/lessons/html-attributes.mdx";
import HtmlElements from "@/content/tracks/web-development/courses/web-development-foundations/modules/html-foundations/lessons/html-elements.mdx";
import HtmlImages from "@/content/tracks/web-development/courses/web-development-foundations/modules/html-foundations/lessons/html-images.mdx";
import HtmlLinks from "@/content/tracks/web-development/courses/web-development-foundations/modules/html-foundations/lessons/html-links.mdx";
import type { ComponentType } from "react";

/**
 * Static MDX import map (decision D-14). Keys are `<moduleId>/<lessonId>.mdx`
 * — matching each lesson JSON's contentPath suffix. The bundler compiles
 * content MDX at build time; no runtime compilation.
 *
 * When a new lesson is added, add its import here. A mismatch between this
 * map and the curriculum tree is caught by the lesson page (notFound) and —
 * in CI — by the SEO/loader tests.
 */
export type MdxComponent = ComponentType<Record<string, unknown>>;

const LESSON_DIR = "html-foundations";

export const mdxMap: Record<string, MdxComponent> = {
  [`${LESSON_DIR}/introduction-to-html.mdx`]: IntroductionToHtml,
  [`${LESSON_DIR}/html-elements.mdx`]: HtmlElements,
  [`${LESSON_DIR}/html-attributes.mdx`]: HtmlAttributes,
  [`${LESSON_DIR}/html-links.mdx`]: HtmlLinks,
  [`${LESSON_DIR}/html-images.mdx`]: HtmlImages,
};

export function getLessonMdx(contentPath: string): MdxComponent | undefined {
  // contentPath is "./<lessonId>.mdx" relative to the lesson JSON; the map
  // key is "<moduleId>/<lessonId>.mdx".
  const normalized = path.normalize(contentPath).replace(/^\.\//, "");
  return mdxMap[`${LESSON_DIR}/${normalized}`] ?? mdxMap[normalized];
}
