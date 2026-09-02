/**
 * Consecutive-day streak computation (PROG-03, 04-CONTEXT D-03).
 *
 * Pure function: derived at read time from progress-event dates — no stored
 * streak state that could drift or be forged. A streak is a run of days with
 * ≥1 event, anchored on today or yesterday (yesterday keeps the streak alive
 * until the day ends; today's event isn't required yet).
 */
export function computeStreak(dates: Date[], now: Date): number {
  if (dates.length === 0) return 0;

  // Calendar-day keys in UTC (documents the simplification; UI copy avoids
  // promising local-midnight precision).
  const dayKey = (d: Date) => d.toISOString().slice(0, 10);

  const days = new Set(dates.map(dayKey));
  if (days.size === 0) return 0;

  // Walk back from the anchor (today; if no event today, yesterday).
  const cursor = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  const DAY_MS = 24 * 60 * 60 * 1000;

  const todayKey = dayKey(cursor);
  const yesterdayKey = dayKey(new Date(cursor.getTime() - DAY_MS));

  if (!days.has(todayKey) && !days.has(yesterdayKey)) return 0;

  const anchor = days.has(todayKey) ? todayKey : yesterdayKey;

  let streak = 0;
  let current = new Date(`${anchor}T00:00:00.000Z`);
  while (days.has(dayKey(current))) {
    streak += 1;
    current = new Date(current.getTime() - DAY_MS);
  }
  return streak;
}
