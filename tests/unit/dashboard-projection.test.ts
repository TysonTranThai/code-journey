import { describe, expect, it } from "vitest";

import sitemap from "@/app/sitemap";
import { noIndexMetadata } from "@/lib/seo";

describe("dashboard privacy (PLAT-07)", () => {
  it("uses no-index metadata", () => {
    const meta = noIndexMetadata("Your Dashboard");
    expect(meta.robots).toEqual({ index: false, follow: false });
  });

  it("is excluded from the sitemap while public lessons remain", () => {
    const urls = sitemap().map((entry) => entry.url);
    // Exact private route (a lesson titled "...dashboard..." is public content
    // and legitimately appears under /learn/...).
    const privatePaths = urls.filter((url) => {
      const p = new URL(url).pathname;
      return p === "/dashboard" || p.startsWith("/dashboard/");
    });
    expect(privatePaths).toEqual([]);
    expect(urls.some((url) => url.includes("/learn/web-development"))).toBe(true);
  });
});
