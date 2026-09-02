# Plan 02-02 Summary: Auth.js v5 Authentication

**Date:** 2026-09-02 · **Status:** Complete · All verification green

## What Was Built

- **Auth.js v5** (next-auth@5.0.0-beta.32, pinned — registry-verified Next 16 peer) with **@auth/drizzle-adapter@1.11.3** on the shared db client
- `src/lib/auth/config.ts` — Credentials provider (email + bcrypt verify, role into JWT), env-gated GitHub provider (`githubProviderEnabled()`; no fabricated dev credentials), `session: { strategy: "jwt" }` (required with Credentials), custom pages `/login`, trustHost; exports handlers/auth/signIn/signOut
- `src/app/api/auth/[...nextauth]/route.ts` — GET/POST handlers
- `src/types/next-auth.d.ts` — role augmentation (Session/User/JWT)
- `src/lib/auth/password.ts` — bcrypt cost 12 wrappers (async + sync)
- `src/lib/auth/reset-token.ts` — 32-byte url-safe raw tokens, sha256-at-rest, 1-hour TTL, single-use check
- `src/lib/auth/guards.ts` — server-only `requireUser()` (redirect to /login) + `requireRole()` (role fetched FRESH from DB, never from the JWT)
- `src/server/actions/auth.ts` — zod-validated actions: loginAction, register (creates user+profile, generic duplicate message — no enumeration), requestPasswordReset (always-generic response; dev transport = console log of the raw link), consumePasswordReset (hash→lookup→unused/unexpired check→password update→usedAt→best-effort session row delete)
- `(auth)` route group: no-index layout + login/register/reset/reset-[token] pages with accessible client forms (labels, aria-describedby, role=alert, autocomplete attrs, min 44px targets, focus rings)
- Adapter compatibility fix: accounts table property names now snake_case (refresh_token etc.) to match Auth.js adapter typing — no DB change (column names were already snake_case)

## Verification (all run)

| Check | Result |
|---|---|
| `pnpm typecheck` | ✓ |
| `pnpm lint` | ✓ 0 problems |
| `pnpm test` | ✓ 35/35 (new: 4 password tests, 4 reset-token tests) |
| GitHub provider gating | ✓ code path returns [] without env vars |
| Adapter types | ✓ DrizzleAdapter accepts all four tables |

## Notes / Decisions Encountered

- No nodemailer installed (optional peer — verified); dev reset link goes to server console
- JWT sessions cannot be server-revoked; reset deletes DB session rows (future DB-session providers) and relies on token TTL — documented in code comments
- user_setup recorded in PLAN: real GitHub OAuth app is optional user action
