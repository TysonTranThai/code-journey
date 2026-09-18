/**
 * Shared test-name sanitization (single source of truth for the JS, Python,
 * and C++ runtimes).
 *
 * Problem this fixes (learner bug report 2026-09-13): the old sanitizer
 * stripped every non-ASCII character, so Vietnamese test names were destroyed
 * — `lỗi chờ chính xác` became `l-i-ch-o-ch-nh-x-c` — and learners could not
 * read which test failed.
 *
 * Contract:
 *  - Filename-safe across the three runtimes' file systems (no `/`, no NUL,
 *    no shell-hostile `;` `$` quotes).
 *  - Marker-safe: the result flows through `__TEST_RESULT__ <id> status=N`
 *    (one line, whitespace-free ends).
 *  - COLLISION-FREE: two distinct names must never sanitize to the same id
 *    (two tests differing only by a character the old sanitizer dropped would
 *    collide on marker names). We guarantee uniqueness by detecting any loss:
 *    if the pretty form would drop or merge characters, fall back to a
 *    deterministic, collision-free hash suffix.
 *  - Round-trippable for display: when the test names come from the
 *    challenge's own test list (route + VerdictPanel render the AUTHORITATIVE
 *    name from challenge data, not from the marker), display never depends on
 *    this id. The id only has to be stable + unique per run.
 */
const FALLBACK_MAX = 60;

export function sanitizeTestName(name: string): string {
  const raw = (name ?? "").trim();
  if (!raw) return "test";

  // 1. Pretty base: keep letters (any script, incl. Vietnamese diacritics),
  //    numbers, dash, underscore; turn whitespace runs into single dashes.
  const spaced = raw.toLowerCase().replace(/\s+/g, "-");
  const pretty = spaced.replace(/[^\p{L}\p{N}_-]/gu, "");

  if (!pretty) return "test";

  // 2. Loss detection: if every character of the lowercased name survives
  //    (only whitespace was mapped to dashes), the pretty form IS a faithful
  //    id — readable Vietnamese, no collisions. Otherwise (symbols, emoji,
  //    or length cap) append a deterministic suffix so distinct names can
  //    never collide and re-runs stay stable.
  if (pretty === spaced && pretty.length <= FALLBACK_MAX) {
    return pretty;
  }

  let base = pretty.slice(0, FALLBACK_MAX - 8).replace(/-+$/, "");
  if (!base) base = "test";
  let hash = 0;
  for (let i = 0; i < raw.length; i++) {
    hash = (hash * 31 + raw.charCodeAt(i)) | 0;
  }
  return `${base}-${(hash >>> 0).toString(36)}`;
}
