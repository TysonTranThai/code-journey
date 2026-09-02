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
    expect(urls.some((url) => url.includes("/dashboard"))).toBe(false);
    expect(urls.some((url) => url.includes("/learn/web-development"))).toBe(true);
  });
});
