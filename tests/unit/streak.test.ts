import { describe, expect, it } from "vitest";

import { computeStreak } from "@/lib/progress/streak";

const DAY = 24 * 60 * 60 * 1000;

/** Fixed "now": 2026-09-02T15:00:00Z. */
const NOW = new Date("2026-09-02T15:00:00.000Z");

describe("computeStreak (pure)", () => {
  it("returns 0 for empty history", () => {
    expect(computeStreak([], NOW)).toBe(0);
  });

  it("returns 0 when the last event is 2+ days old", () => {
    const dates = [new Date(NOW.getTime() - 3 * DAY), new Date(NOW.getTime() - 2 * DAY)];
    expect(computeStreak(dates, NOW)).toBe(0);
  });

  it("counts a single event today", () => {
    expect(computeStreak([NOW], NOW)).toBe(1);
  });

  it("counts a single event yesterday (streak stays alive until day ends)", () => {
    expect(computeStreak([new Date(NOW.getTime() - DAY)], NOW)).toBe(1);
  });

  it("counts consecutive days ending today", () => {
    const dates = [NOW, new Date(NOW.getTime() - DAY), new Date(NOW.getTime() - 2 * DAY)];
    expect(computeStreak(dates, NOW)).toBe(3);
  });

  it("resets at a one-day gap", () => {
    const dates = [
      NOW,
      new Date(NOW.getTime() - DAY),
      // gap at -2 days
      new Date(NOW.getTime() - 3 * DAY),
    ];
    expect(computeStreak(dates, NOW)).toBe(2);
  });

  it("ignores duplicate events on the same day", () => {
    const morning = new Date("2026-09-02T01:00:00.000Z");
    const evening = new Date("2026-09-02T22:00:00.000Z");
    const yesterday = new Date(NOW.getTime() - DAY);
    expect(computeStreak([morning, evening, yesterday], NOW)).toBe(2);
  });

  it("handles multiple events per day across timezones consistently (UTC days)", () => {
    // A user in UTC+13 landing "tomorrow" UTC still maps to a UTC day key.
    const lateNightUtc = new Date("2026-09-01T23:59:00.000Z");
    const todayUtc = new Date("2026-09-02T00:01:00.000Z");
    expect(computeStreak([lateNightUtc, todayUtc], NOW)).toBe(2);
  });
});
