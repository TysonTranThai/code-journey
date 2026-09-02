import { describe, expect, it } from "vitest";

import { getLinearLessons, getTracks } from "@/lib/curriculum/loaders";
import { noIndexMetadata } from "@/lib/seo";
import sitemap from "@/app/sitemap";
import robots from "@/app/robots";

describe("SEO: no-index helper (PLAT-07)", () => {
  it("marks private pages as index:false, follow:false", () => {
    const meta = noIndexMetadata("Log in");
    expect(meta.robots).toEqual({ index: false, follow: false });
    expect(meta.title).toBe("Log in");
  });
});

describe("SEO: sitemap generated from curriculum loaders", () => {
  const entries = sitemap();
  const urls = entries.map((e) => e.url);

  it("includes the landing and learn index pages", () => {
    expect(urls).toContain("http://localhost:3000/");
    expect(urls).toContain("http://localhost:3000/learn");
  });

  it("includes the track, course, and every lesson page", () => {
    expect(urls).toContain("http://localhost:3000/learn/web-development");
    expect(urls).toContain(
      "http://localhost:3000/learn/web-development/web-development-foundations",
    );
    const lessons = getLinearLessons("web-development");
    expect(lessons).toHaveLength(5);
    for (const lesson of lessons) {
      expect(urls).toContain(
        `http://localhost:3000/learn/web-development/${lesson.courseId}/${lesson.moduleId}/${lesson.id}`,
      );
    }
  });
});

describe("SEO: robots rules", () => {
  const result = robots();
  const rule = Array.isArray(result.rules) ? result.rules[0] : result.rules;
  const allow = Array.isArray(rule?.allow) ? rule.allow.join(" ") : String(rule?.allow ?? "");
  const disallow = Array.isArray(rule?.disallow)
    ? rule.disallow.join(" ")
    : String(rule?.disallow ?? "");

  it("allows public content and disallows the API", () => {
    expect(allow).toContain("/");
    expect(disallow).toContain("/api/");
  });

  it("points at the sitemap", () => {
    expect(result.sitemap).toBe("http://localhost:3000/sitemap.xml");
  });
});

describe("SEO: curriculum is loaders-driven (structure sanity)", () => {
  it("track exposes exactly the seed course", () => {
    const tracks = getTracks();
    expect(tracks).toHaveLength(1);
    expect(tracks[0]?.courses[0]?.reference).toBe("web-development-foundations");
  });
});
