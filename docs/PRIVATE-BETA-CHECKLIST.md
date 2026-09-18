# Private Beta Checklist (Phase 9 — updated 2026-09-05)

Legend: **GREEN** verified working · **YELLOW** works with an accepted beta
limitation · **RED** unsafe/broken/unverified. Every status below is backed by
an executed verification (see docs/DEPLOYMENT.md and the Phase 9 report).

**User decisions (2026-09-05):** dev machine approved as the private-beta host;
ngrok tunnel verified then stood down — beta serves localhost-only for now;
custom domain deferred; email + AI mentor deferred.

## Infrastructure

| Item                | Status     | Notes                                                                                                                            |
| ------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Web host            | **GREEN**  | User-approved dev machine; beta stack (db/web/worker) running healthy in containers                                              |
| Database            | **GREEN**  | Postgres 16, migrations apply cleanly from scratch (double-PK defect fixed), healthchecked, no public exposure                   |
| Sandbox host        | **YELLOW** | Live single-host fallback (worker + local socket on the beta host); two-host split remains the production target                 |
| Worker              | **GREEN**  | Containerized worker verified end-to-end; healthcheck; kill-switch = stop worker                                                 |     | Reverse proxy / HTTPS | **YELLOW** | Serving loopback-only (http://localhost:3000) per user decision; the ngrok HTTPS path was fully verified (TLS, headers, E2E 30/30) then stood down; re-enable procedure documented in docs/DEPLOYMENT.md |
| DNS / domain        | **YELLOW** | Not required for loopback beta; custom domain deferred by user                                                                   |
| Beta access control | **GREEN**  | Invite gate verified: correct code works; wrong code creates 0 accounts (live, server-side); E2E passes through tunnel with code |

## Application

| Item                | Status    | Notes                                                                            |
| ------------------- | --------- | -------------------------------------------------------------------------------- |
| Production env vars | **GREEN** | `.env.example` is the complete inventory; secrets env-only, never in images      |
| Database migrations | **GREEN** | `migrate` one-shot profile; backup required before runs                          |
| Build               | **GREEN** | `next build` 121 pages; container build verified (build-stage placeholders only) |
| Start               | **GREEN** | `pnpm start` / container CMD; loopback-only port binding by default              |
| Health checks       | **GREEN** | `/health` + compose healthchecks (web/worker/db)                                 |

## Security

| Item                        | Status     | Notes                                                                                       |
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------- |
| Auth required for execution | **GREEN**  | Live: anonymous run → 401, no job enqueued                                                  |
| Submission ownership        | **GREEN**  | Live: non-owner → 401/404; integration suite green                                          |
| Rate limiting               | **GREEN**  | Live: burst limit → 429 on 6th run; atomic limiter integration-tested                       |
| Sandbox isolation           | **GREEN**  | Full attack-class suite green (fork bomb, egress, fs escape, loop, memory, grade integrity) |
| Sandbox leak fix            | **GREEN**  | Wall-clock kill now stops the container; 0 leaks across 3 verification runs                 |
| Secret isolation            | **GREEN**  | `.dockerignore` blocks env files; worker env has no user-data credentials                   |
| Security headers            | **GREEN**  | CSP/nosniff/frame-deny/referrer/permissions verified live on every response                 |
| Secure cookies              | **GREEN**  | `secure` in production; httpOnly; sameSite=lax                                              |
| HTTPS                       | **YELLOW** | Live via ngrok tunnel (real TLS); custom domain deferred for beta                           |
| Session expiration          | **YELLOW** | JWT expiry only; server-side revocation impossible by design (documented)                   |
| Email verification          | **YELLOW** | Not implemented; registration is invite-gated instead                                       |

## Email

| Item           | Status     | Notes                                                                                  |
| -------------- | ---------- | -------------------------------------------------------------------------------------- |
| Provider       | **YELLOW** | SMTP adapter implemented + env-gated; real delivery UNVERIFIED until credentials exist |
| Password reset | **YELLOW** | Enumeration-safe flow works; without SMTP the link is console-only (documented)        |

## AI

| Item            | Status     | Notes                                                                          |
| --------------- | ---------- | ------------------------------------------------------------------------------ |
| Mentor provider | **YELLOW** | No key configured; NullMentor degradation verified — platform fully functional |

## Course (Course 1 — Web Development Beginner)

| Item                                                | Status    | Notes                                                       |
| --------------------------------------------------- | --------- | ----------------------------------------------------------- |
| 7 modules / 56 lessons / 51 challenges / 5 projects | **GREEN** | Integrity suite 34 checks; 121 pages built; 60 sitemap URLs |
| Progress / checkpoints / achievements               | **GREEN** | Server-verified; live run recorded progress                 |
| Anonymous browsing                                  | **GREEN** | Public curriculum readable without account (live-verified)  |

## QA

| Item                      | Status    | Notes                                                                                      |
| ------------------------- | --------- | ------------------------------------------------------------------------------------------ |
| Unit + integration        | **GREEN** | 128/128 (incl. sandbox isolation suite)                                                    |
| E2E                       | **GREEN** | 30/30 (critical path, keyboard-only, axe AA, mobile)                                       |
| Live security regression  | **GREEN** | 20/20 checks on the production build (headers, authz, rate limit, ownership, learner loop) |
| E2E through deployed beta | **GREEN** | 30/30 via public HTTPS URL incl. invite-gated registration and mobile viewports            |
| Typecheck / lint / format | **GREEN** | All clean                                                                                  |
| Backup / restore          | **GREEN** | pg_dump verified + restore-verified into fresh Postgres                                    |
| Manual learner smoke test | **GREEN** | Register(gated) → learn → run → pass → persist verified live                               |
| Mobile                    | **GREEN** | E2E at 7 viewports incl. 375px (mobile editor + run flow)                                  |
| Accessibility             | **GREEN** | axe AA audits on core flows in E2E                                                         |

## Beta gate summary

**Zero RED items.** Accepted YELLOW limitations (all explicitly approved for
private beta): ephemeral tunnel URL instead of a custom domain; single-host
sandbox fallback; unverified SMTP delivery (password reset link is console-only
until an SMTP provider is configured); no AI mentor provider (graceful
degradation); JWT sessions without server-side revocation; no email
verification (invite gate instead); no external monitoring.

**Verdict: PRIVATE BETA = GO (localhost-only)** — the deployed beta serves at
http://localhost:3000 (user decision; remote access intentionally off). The
learner loop was verified end-to-end both on loopback and through the (since
stopped) HTTPS tunnel: register with invite → learn → run → verdict → persist.
All security gates green; backup/restore proven; rollback + worker kill-switch
documented. Note: with remote access off, "beta users" are limited to people
using this machine until the tunnel or a domain is re-enabled.

**PUBLIC PRODUCTION: NOT READY** — Judge0 migration, dedicated sandbox host,
real domain, verified email delivery, production monitoring, and final security
review all remain (docs/PRODUCTION.md).
