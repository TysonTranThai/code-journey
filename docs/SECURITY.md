# Security

**Status as of 2026-09-03 (milestone v1 complete).** This document is deliberately honest:
every control below is marked VERIFIED (with the evidence that proves it), PARTIAL
(what exists and what is missing), PLANNED, or DEFERRED. Nothing is claimed secure
beyond what a test or live verification in this repository demonstrates.

## Implemented — verified

| Control                           | Evidence                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sandbox isolation                 | `tests/integration/sandbox-isolation.test.ts` (7 tests, all green): fork bomb killed by PID cap, network egress denied (`--network none`), filesystem escape contained (read-only root + tmpfs scratch), infinite loop and memory bomb killed by wall-clock/CPU/memory limits; normal pass/fail flows unaffected. Runner uses the full hardening flag set (`src/workers/sandbox.ts`) |
| Execution off the web tier        | The web tier never spawns interpreters. Student code reaches execution only via `POST /api/challenges/run` → Postgres queue → `pnpm worker` → sandbox container (`src/workers/execute.ts`). Job payloads carry code + tests + limits only — no env vars or secrets (type-enforced via `JobPayload`)                                                                                  |
| Authentication                    | Auth.js (next-auth 4) credentials provider, bcrypt password hashing, JWT sessions with `id` + `role` claims (`src/lib/auth/config.ts`). Live-verified end-to-end: register → login → session cookie (`httpOnly`, `sameSite=lax`, `secure` in production) → logout (E2E `tests/e2e/critical-path.spec.ts`)                                                                            |
| Authorization                     | `requireUser()` / `requireRole()` (`src/lib/auth/guards.ts`): roles are fetched **fresh from the database** on every check, never trusted from the JWT alone; anonymous users are redirected to `/login`; protected pages redirect server-side (dashboard E2E verifies both branches)                                                                                                |
| Input validation                  | Zod schemas at every trust boundary: all API routes (`/api/auth/*`, `/api/challenges/*`, `/api/progress/*`), all server actions (discussions, mentor), and the entire curriculum content pipeline (invalid content fails the build — `tests/unit/curriculum-loaders.test.ts`)                                                                                                        |
| XSS posture                       | React auto-escaping everywhere; **zero** `dangerouslySetInnerHTML` usages in `src/` (verified by repo search 2026-09-03); MDX is restricted to repo-reviewed content files; discussion/mentor text renders as plain React text nodes                                                                                                                                                 |
| SQL injection                     | Drizzle ORM exclusively — parameterized queries, no string-built SQL anywhere in `src/`                                                                                                                                                                                                                                                                                              |
| CSRF                              | Auth.js built-in CSRF protection on auth endpoints (CSRF token + cookie double-submit, exercised in E2E); Next.js Server Actions verify request origin                                                                                                                                                                                                                               |
| Secret hygiene                    | `.gitignore` excludes all `.env*local*` variants; only `.env.example` with placeholders is committed; the mentor provider key is read server-side only and absent means the NullMentor graceful mode (no crash, no key exposure)                                                                                                                                                     |
| Dependency audit                  | `pnpm audit` → **0 vulnerabilities** (2026-09-03) after two pinned overrides (`dompurify@<3.4.7` → `>=3.4.7` via monaco-editor chain, `esbuild@<=0.24.2` → `>=0.25.0` via drizzle-kit's deprecated `@esbuild-kit` chain — both dev-impact verified: build, migrations, and tests all green post-override)                                                                            |
| Observability (no secret leakage) | `src/lib/observability.ts`: structured JSON logs with a redaction pass over key names matching `/password                                                                                                                                                                                                                                                                            | token | secret | authorization | cookie | apikey/i`; the runner logs job ids and statuses only — never payload code, env, or secrets |
| Health endpoint                   | `/health` returns non-sensitive status JSON only (no env dumping)                                                                                                                                                                                                                                                                                                                    |

## Partial (honest gaps)

| Area          | What exists                                                                                                                            | What is missing                                                                                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rate limiting | Mentor requests: per-user + per-IP quotas persisted in Postgres with a 24h window (`src/lib/mentor/rate-limit.ts`, integration-tested) | Challenge run submissions and auth attempts are not yet rate-limited (queued execution and Auth.js provide _some_ natural throttling, but explicit limits belong in the production-hardening pass) |
| SSRF posture  | Sandbox has **no network** (verified); the app currently makes no arbitrary outbound requests                                          | An outbound allow-list must be added before any feature (webhooks, AI provider) makes server-side HTTP calls                                                                                       |

## Planned

| Area                         | Plan                                                                                                                                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Production sandbox evolution | The current hardened-Docker sandbox is the dev baseline. For production, evaluate self-hosted Judge0 or Firecracker microVMs (E2B/Vercel Sandbox class) against the chosen host — decision deliberately deferred to deployment planning |
| Auth hardening               | Email verification + password reset flows, GitHub OAuth (requirement PLAT-04), session rotation strategy                                                                                                                                |
| Admin surface                | Role checks exist (`requireRole`), but no admin UI ships in v1; when it does, every admin route gets an integration test proving URL-guessing fails                                                                                     |

## Deferred

- **File uploads** — no upload feature exists; any future design needs type/size allowlists, AV scanning, and storage isolation before shipping.
- **Production infrastructure security** — nothing is deployed yet; headers, TLS, and secret management are configured at deployment time.

## Reporting

Security issues: open a private security advisory (do not open public issues for
exploitable behavior).
