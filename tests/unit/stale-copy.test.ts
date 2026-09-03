import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * Stale-copy guard (07-05).
 *
 * Public-facing pages must not claim shipped features are still pending. This
 * scans every route page in src/app for the known stale phrases and fails if
 * any reappear. Scope is deliberately user-facing pages only — planning
 * artifacts (.planning/) and docs (docs/SECURITY.md "PLANNED"/"DEFERRED"
 * statuses) legitimately use forward-looking language.
 */

function collectPageFiles(dir: string, acc: string[] = []): string[] {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      collectPageFiles(full, acc);
    } else if (entry === "page.tsx") {
      acc.push(full);
    }
  }
  return acc;
}

const STALE_PHRASES = [
  "upcoming phases",
  "arriving in a later phase",
  "coming soon",
  "will ship",
  "in a future phase",
];

const pageFiles = collectPageFiles(join(process.cwd(), "src/app"));

describe("stale product copy guard (07-05)", () => {
  it("finds route pages to scan (sanity)", () => {
    expect(pageFiles.length).toBeGreaterThan(5);
  });

  for (const phrase of STALE_PHRASES) {
    it(`no page claims shipped features "${phrase}"`, () => {
      const offenders = pageFiles.filter((f) =>
        readFileSync(f, "utf8").toLowerCase().includes(phrase),
      );
      expect(offenders, `stale copy in: ${offenders.join(", ")}`).toEqual([]);
    });
  }

  it("homepage affirmatively describes shipped features", () => {
    const home = readFileSync(join(process.cwd(), "src/app/page.tsx"), "utf8");
    expect(home).toMatch(/auto-graded challenges/i);
    expect(home).toMatch(/progress tracking/i);
    expect(home).toMatch(/mentor/i);
  });
});
