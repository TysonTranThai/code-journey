---
phase: 07-beta-readiness-hardening
status: planning
---

# Phase 7: V1.1 Beta Readiness & Hardening — Context

**Gathered:** 2026-09-03
**Status:** Ready for planning

## Phase Boundary

Phase 7 hardens the complete V1 milestone toward a controlled **private beta**. It fixes
concrete blockers surfaced by the V1 product audit. It does NOT expand the curriculum,
add product features, or redesign unrelated parts.

- **In scope:** the P0 must-fix blockers and the priority-P1 hardening items.
- **Explicitly out of scope:** curriculum expansion (CSS/JS/content breadth), new major
  product features, and the P2 future items (thread-lesson validation, SSRF allow-list,
  CSP/security headers, DB backups, pooling, metrics) — P2 items are only addressed where
  Phase 7 implementation forces them.

## Verified Audit Baseline (confirmed against current code, 2026-09-03)

- V1 milestone committed; 34/34 requirements, 19/19 plans, 94/94 unit/integration,
  13/13 Playwright E2E, `pnpm audit` clean, typecheck/lint/format clean, sandbox
  malicious-sample suite green.
- Every audit finding below was **re-verified against the source** before planning.

## Finding → work mapping

| ID | Finding | Verified in code | Phase 7 plan |
|----|---------|------------------|--------------|
| P0-01 | Mobile/tablet challenge editor renders 0×0 | `ChallengeWorkspace.tsx` (`lg:hidden` wrapper has no definite height → `h-full`/`flex-1` chain collapses; Monaco mounts in a `display:none` tab panel and `automaticLayout` can't recover) | 07-06 |
| P0-02 | Stale/false product copy ("ship in upcoming phases" / "arriving in a later phase") | `src/app/page.tsx:31`, `src/app/(learn)/learn/page.tsx:24`; also `/learn` metadata over-promises "HTML, CSS, JavaScript" | 07-05 |
| P0-03 | Grade-integrity heredoc escape (fixed `CODEJOURNEY_EOF` delimiter) | `src/workers/sandbox.ts` `buildJobScript`/`heredoc` | 07-01 |
| P0-04 | Password reset logs link to server console only | `src/server/actions/auth.ts` `requestPasswordReset`; mechanics already correct (`reset-token.ts`: hashed, 1h TTL, single-use, enumeration-safe) | 07-04 |
| P1-01 | No rate limiting on register/login/reset/run; mentor check+record non-atomic | `src/server/actions/auth.ts`, `src/app/api/challenges/run/route.ts`, `src/lib/mentor/rate-limit.ts` | 07-03 |
| P1-02 | Submission IDOR: `GET /api/challenges/run/[submissionId]` has no auth/ownership | `src/app/api/challenges/run/[submissionId]/route.ts` | 07-02 |
| P1-03 | Docker-socket worker unsuitable for public production | `src/workers/sandbox.ts` (spawns `docker ... run`); `docs/SECURITY.md` | 07-10 |
| P1-04 | All routes dynamic because `SiteHeader` calls `auth()` in root layout | `src/components/layout/SiteHeader.tsx`, `src/app/layout.tsx` | 07-08 |
| P1-05 | Mobile run flow: Run button only in Instructions tab | `src/components/challenge/ChallengeWorkspace.tsx` (mobile tab content) | 07-07 |
| P1-06 | Challenge breadcrumb shows course slug; prompts render literal backticks | challenge page `Breadcrumbs` uses `courseId`; `ChallengeWorkspace` renders prompt in a `<p>` | 07-09 |

## Standing constraints (unchanged)

- WEB-ONLY product; responsive web first; server-side execution/AI behind APIs; no native
  targets. SEO for public content; no-index for private data. No vendor lock-in.
- Arbitrary student code never executes on the web tier.
- WCAG 2.1 AA is a requirement.
- Do not choose a hosted provider (email, rate-limit, AI, execution) without justification;
  prefer adapters/interfaces.

## Resolved decisions (2026-09-03)

- **Auth required to run — DECIDED YES.** Code execution requires an authenticated account.
  Anonymous users keep read access to public curriculum/challenge instructions but cannot
  submit code (07-02).
- **Production execution — DECIDED self-hosted Judge0.** Local = hardened Docker; private
  beta = hardened Docker on a dedicated sandbox worker host (isolated from the web host, no
  shared Docker socket); public production = dedicated Judge0 host isolated from web app, DB,
  and secrets. Phase 7 only implements the beta-safe boundary and documents the production
  migration + Judge0 security requirements checklist (07-10); no production infra is stood up
  in Phase 7.
