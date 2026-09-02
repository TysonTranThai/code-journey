# Phase 0 Report — Environment + Development Foundation

**Date:** 2026-09-02 · **Project:** Code Journey · **Repo:** `/Users/tysontran/Documents/Code Journey` (branch `main`, 7 commits)

## ENVIRONMENT

| Item | Value |
|------|-------|
| OS | macOS 26.6.2 (arm64) |
| CPU | Apple M4, 10 cores, 16 GB RAM |
| Node.js | 22.22.2 |
| Package manager | **pnpm 10.4.0** (npm 10.9.7, yarn 1.22.22, bun 1.3.12 also present) |
| Python | 3.9.6 (Apple CLT; not used by this project) |
| Docker | 29.5.2 + Compose v5.1.3 (installed; daemon not running at audit time) |
| Database | PostgreSQL 16.13 client (server not running; project uses Docker from Phase 2) |
| Git | 2.50.1 |

## PROJECT

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 16.3.4 (App Router) + React 19.2.8 + Tailwind CSS 4.3.3 |
| Backend | Same Next.js modular monolith (route handlers/server actions), module seams for future services |
| Database | PostgreSQL 16 (Docker Compose, port 5433) + Drizzle ORM 0.45 — Phase 2 |
| Authentication | Auth.js (NextAuth v5 line) pattern: email/password + GitHub OAuth — Phase 2 |
| AI | Provider-agnostic `MentorAdapter` with pedagogy-first guardrails; platform fully functional without a key — Phase 5 |
| Code execution | Isolated sandbox (Judge0-style hardening baseline; isolation tech decided at Phase 3 planning) — **never on the web tier** — Phase 3 |
| Testing | Vitest 4 (unit/integration) + Playwright 1.62 (E2E, Phase 6) |
| Deployment | None yet (intentional) — Docker Compose locally; production path decided in Phase 6 |

## INSTALLED

next@16.3.4, react@19.2.8, react-dom@19.2.8, zod@4.5.4 · devDeps: typescript@~6.0.3,
tailwindcss@4.3.3, @tailwindcss/postcss@4.3.3, @types/node@22, @types/react@19.2.18,
@types/react-dom@19.2.5, eslint@~9.39.5, eslint-config-next@16.3.4, prettier@3.9.6,
vitest@4.1.11. Project artifacts: tsconfig (strict), eslint flat config, vitest config,
prettier config, postcss config, next config, `.gitignore`, `.env.example`, README,
CONTRIBUTING, docs/ (ARCHITECTURE, DATA-MODEL, SECURITY, ACCESSIBILITY, ENVIRONMENT,
this report), GSD planning suite in `.planning/` (PROJECT, REQUIREMENTS, ROADMAP,
STATE, config, 5 research docs).

## VERIFIED (all commands actually run and passing on 2026-09-02)

| Command | Result |
|---------|--------|
| `pnpm install` / `pnpm install --frozen-lockfile` | ✓ (8.3s fresh; 288ms frozen) |
| `pnpm typecheck` | ✓ strict TS, zero errors |
| `pnpm lint` | ✓ ESLint flat config, zero errors |
| `pnpm test` | ✓ Vitest: 2/2 tests pass |
| `pnpm build` | ✓ Next.js production build compiles; 3 routes generated |
| `pnpm dev` | ✓ dev server on :3000; `/health` → 200 JSON; landing → 200 with skip link |
| `pnpm start` | ✓ prod server on :3000; `/health` → 200; landing → 200 |
| `pnpm format` / `pnpm format:check` | ✓ Prettier clean |
| Git workflow | ✓ `main` branch, 7 atomic commits, clean status, secrets excluded |

## FAILED (and resolution)

| Issue | Resolution |
|-------|------------|
| `@types/react-dom@^19.2.8` doesn't exist (types version independently) | Pinned to registry-verified 19.2.5 |
| typescript-eslint does not support TypeScript 7.0 (new Go-based compiler) | Pinned TypeScript to 6.0.3 (newest supported); documented for future revisit |
| eslint-plugin-react (via eslint-config-next) crashes under ESLint 10 | Pinned ESLint to 9.39.5 (npm `latest` 10.9.1 marked deprecated by Next's own config) |
| `eslint-config-next@16` no longer exports `configs["core-web-vitals"]` | Rewrote flat config to its new subpath exports (`/core-web-vitals`, `/typescript`) |
| `pnpm start` bound to a stray `PORT` env var (58799) in this shell instead of 3000 | `next start --port 3000` pinned in package.json |
| Next.js warning about `package-lock.json` in `$HOME` | `outputFileTracingRoot` pinned to the repo in next.config.ts |

## UNKNOWN

- **Auth.js package/version:** npm `latest` for `next-auth` is the v4 line (4.24.15);
  the v5 App Router line is still beta-tagged. Exact choice and version are decided
  with verification at Phase 2 implementation. Fallback alternatives documented in
  `.planning/research/STACK.md`.
- **Sandbox isolation technology** (hardened Docker vs gVisor vs Firecracker vs
  self-hosted Judge0): deliberately open until the Phase 3 deployment target is known.
- **AI provider:** intentionally undecided; the adapter interface is specified, no
  provider key exists, nothing was assumed.
- **Remote git origin:** none configured (repo is local-only); push target is a user
  decision.

## RISKS

1. **Execution sandbox security (highest):** untrusted code execution is the platform's
   defining risk. Mitigation: no student code runs anywhere yet; Phase 3 requires an
   isolation checklist + malicious-sample suite before any claim of security.
2. **16 GB RAM / single dev machine:** sandbox container pools and Firecracker-style
   microVM testing may be constrained locally; Phase 3 planning must validate realistic
   concurrency on this hardware.
3. **Fresh toolchain (Next 16 / TS 6 / Tailwind 4):** bleeding-edge majors carry
   ecosystem-compatibility risk, as today's two lint failures demonstrated; both were
   resolved by pinning to supported lines, and exact versions are locked in
   `pnpm-lock.yaml`.
4. **TypeScript 7 (Go-based) is incompatible with the lint stack** — revisit when
   typescript-eslint ships ≥7.1 support.
5. **Port collisions** (3001/5173 occupied on this machine): mitigated by pinning 3000
   and documenting alternatives.
6. **Single-maintainer bus factor:** mitigated by GSD planning docs + this documentation.

## NEXT PHASE (recommended — do not start automatically)

**Phase 1 execution is already complete as part of this initialization** (scaffold,
quality gates, git hygiene, docs — see `.planning/ROADMAP.md` Phase 1; success criteria
1–4 are verified above). Recommended next:

**Phase 2 — Data, Auth & Content Pipeline:** PostgreSQL via Docker Compose + Drizzle
schema (users/sessions/curriculum core), Auth.js email/password + GitHub with dev email
transport, content-as-data pipeline (MDX/JSON + zod build-time validation), and the
curriculum browsing UI. Requirements covered: AUTH-01…05, CURR-01…04.

Start it with: `$gsd-plan-phase 2` (or `$gsd-discuss-phase 2` to clarify approach first).
