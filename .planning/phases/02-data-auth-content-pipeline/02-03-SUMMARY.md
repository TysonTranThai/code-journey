# Plan 02-03 Summary: Content-as-Data Pipeline + Seed Curriculum

**Date:** 2026-09-02 · **Status:** Complete · All verification green

## What Was Built

- `src/lib/curriculum/schema.ts` — zod 4 schemas (track/course/module/lesson): slug-id pattern, bounded minutes (1–240), difficulty enum, explicit child ordering via `{ reference }`, `challenges` array (empty in Phase 2), inferred types + `ResolvedLesson`
- `src/lib/curriculum/loaders.ts` — validated loaders with injectable root: per-file schema parse (errors carry file path + zod issue path), cross-reference checks (missing referenced files, dangling contentPath, path-escape guard), global id uniqueness, module-level cache, `CurriculumNotFoundError`; accessors getTracks/getTrack/getCourse/getCurriculumModule/getLesson/getLinearLessons/getLinearNeighbors/readLessonBody
- Seed curriculum `src/content/tracks/web-development/` — track Web Development → course Web Development Foundations → module HTML Foundations → 5 real MDX lessons (Introduction to HTML, Elements, Attributes, Links, Images), each 300+ words with code examples and a "What you learned" recap
- `tests/fixtures/content-invalid/` — 4 invalid trees (missing field, duplicate id, broken contentPath, empty lessons), each an independently loadable `tracks/` root
- Tests: 9 schema + 9 loader (positive, negative, neighbors, body read)

## Verification (all run)

| Check | Result |
|---|---|
| `pnpm typecheck` | ✓ |
| `pnpm test` | ✓ 28/28 (incl. 4 invalid-content cases that must throw) |
| Loader smoke via tsx | ✓ 1 track, 5 lessons, correct neighbor pairs |
| Uniqueness guard live-fire | ✓ caught the initial track/course id collision during development |

## Notes / Decisions Encountered

- Track id is `web-development`, course id `web-development-foundations` — global id uniqueness forbids reusing the same id for track and course (the guard caught this on first run)
- Fixtures nest each case under `tracks/<track-id>/` so a single case is a valid loader root
- CURR-04 build-failure behavior: loaders validate at module load; any page importing them makes `pnpm build` fail on invalid content (negative cases proven at unit level)
