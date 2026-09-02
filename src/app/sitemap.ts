import type { MetadataRoute } from "next";

import { getLinearLessons, getTracks } from "@/lib/curriculum/loaders";
import { siteConfig } from "@/lib/site-config";

/**
 * Sitemap for all public, indexable pages (PLAT-07). Curriculum URLs are
 * generated from the validated content loaders — a new lesson in content
 * appears here automatically.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const base = siteConfig.url;
  const entries: MetadataRoute.Sitemap = [{ url: `${base}/` }, { url: `${base}/learn` }];

  for (const track of getTracks()) {
    entries.push({ url: `${base}/learn/${track.id}` });
    for (const lesson of getLinearLessons(track.id)) {
      entries.push({
        url: `${base}/learn/${track.id}/${lesson.courseId}/${lesson.moduleId}/${lesson.id}`,
      });
    }
    // Course overview pages are also public and indexable.
    for (const courseRef of track.courses) {
      entries.push({ url: `${base}/learn/${track.id}/${courseRef.reference}` });
    }
  }

  return entries;
}
