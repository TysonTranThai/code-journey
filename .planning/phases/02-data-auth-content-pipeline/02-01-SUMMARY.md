# Plan 02-01 Summary: PostgreSQL + Drizzle Identity Layer

**Date:** 2026-09-02 · **Status:** Complete · All verification green

## What Was Built

- `docker-compose.yml` — postgres:16-alpine on localhost:5433, named volume, healthcheck
- `drizzle.config.ts` — reads DATABASE_URL (manual .env.local parse; clear error when missing)
- `src/lib/db/schema.ts` — six identity tables: users (role enum student/admin, nullable passwordHash), accounts, sessions, verification_tokens, password_reset_tokens (sha256 hash at rest, unique), profiles; cascade FKs
- `src/lib/db/index.ts` — server-only drizzle client singleton (postgres-js, pool 10, 5s connect timeout)
- `src/lib/db/seed.ts` — idempotent dev fixtures (dev-student + dev-admin, bcrypt cost 12)
- db scripts: db:up / db:down / db:reset / db:generate / db:migrate / db:seed / db:studio
- `vitest.config.ts` — loads .env.local so integration tests can reach the DB
- Tests: unit schema assertions (no DB) + DB-guarded integration suite (skips when DB down)
- README: Database section documenting every db: command

## Verification (all run)

| Check | Result |
|---|---|
| `docker compose up -d db` → healthy | ✓ (~9s, port 5433) |
| `pnpm db:generate` | ✓ migration 0000_salty_groot.sql committed |
| `pnpm db:migrate` from clean volume | ✓ 6 tables created |
| `pnpm db:seed` (twice via integration test) | ✓ idempotent, 1 row per email |
| `pnpm typecheck` | ✓ |
| `pnpm test` | ✓ 11/11 (7 unit + 4 integration) |
| bcrypt verify right/wrong password | ✓ |

## Notes / Decisions Encountered

- `@types/bcryptjs` NOT installed — bcryptjs 3.0.3 ships its own types (verified)
- Vitest needed explicit .env.local loading (config updated)
- Integration suite skips itself (verified) when the DB is unreachable — keeps `pnpm test` green without Docker
- No curriculum/progress/submission tables created — DB stores identity only (decision D-09)
