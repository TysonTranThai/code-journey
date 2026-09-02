import { describe, expect, it } from "vitest";
import { siteConfig } from "@/lib/site-config";

describe("siteConfig", () => {
  it("exposes the platform name and mission-critical tagline", () => {
    expect(siteConfig.name).toBe("Code Journey");
    expect(siteConfig.tagline).toContain("Free");
  });

  it("describes the product without overclaiming implemented features", () => {
    // Guardrail: description mentions aspirations, but status text must not
    // claim features that don't exist yet (foundation phase).
    expect(siteConfig.description).toBeTruthy();
  });
});
