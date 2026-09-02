# Stack Research

**Domain:** Coding education platform (online judge + LMS + community)
**Researched:** 2026-09-02
**Confidence:** HIGH (versions verified live from npm registry on research date; domain patterns from current ecosystem sources)

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Next.js (App Router) | 16.3.4 | Full-stack web framework | Current major; React 19, RSC, server actions, API routes — one deployable for UI + API (modular monolith) |
| React | 19.2.8 | UI runtime | Pairs with Next 16; stable current line |
| TypeScript | 7.0.2 | Type safety platform-wide | Non-negotiable for a platform with student code, graders, and money-free trust surface |
| Tailwind CSS | 4.3.3 | Design system foundation | v4 CSS-first config; fast iteration for a custom, non-corporate look |
| Drizzle ORM | 0.45.2 (drizzle-kit 0.31.10) | PostgreSQL data access | 2026 ecosystem lean for new Next.js projects: TS-native schema, SQL-faithful, no codegen step; Prisma latest tag currently points to an RC (8.0.0-rc.12) |
| PostgreSQL 16 | 16.13 (installed locally) | Primary database | Relational fit for users/progress/submissions; JSONB where content is flexible |
| Auth.js (NextAuth v5 line) | next-auth 4.24.15 is the stable npm tag | Authentication | Email/password + OAuth (GitHub/Google) + sessions; v5 beta for App Router — decision deferred to implementation phase, documented in UNKNOWN |
| Vitest | 4.1.11 | Unit/integration tests | Current major; native TS, fast, same runner for web + runner packages |
| Playwright | 1.62.1 (@playwright/test) | E2E tests | Cross-browser; needed for a-11y and critical-path verification |
| ESLint (flat config) | 10.9.1 + eslint-config-next 16.3.4 | Linting | Current major, flat config standard |
| Zod | 4.5.4 | Schema validation | Runtime validation at API boundaries and env parsing |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @tailwindcss/postcss | 4.3.3 | Tailwind v4 PostCSS pipeline | From first render |
| Docker + Docker Compose | 29.5.2 / v5.1.3 (installed) | Local Postgres, later sandbox prototyping | From db setup onward |

## Installation

```bash
pnpm add next@16 react@19 react-dom@19
pnpm add -D typescript@7 @types/node @types/react @types/react-dom
pnpm add -D tailwindcss@4 @tailwindcss/postcss@4
pnpm add drizzle-orm@0.45 zod@4
pnpm add -D drizzle-kit@0.31
pnpm add -D eslint@10 eslint-config-next@16
pnpm add -D vitest@4 @playwright/test@1.62
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Drizzle ORM | Prisma 7.x stable (7.10.0) | If team prefers DSL + codegen DX; note `latest` tag currently serves an RC |
| Drizzle ORM | Prisma 6.x | If Prisma 7 docs/migration story feels too fresh at build time |
| Next.js monolith | Separate Fastify/Hono API + Vite SPA | If backend later needs independent scaling or non-Node services dominate |
| Auth.js | Better Auth / Lucia / Clerk | Re-evaluate at auth implementation phase; Clerk adds cost + vendor lock-in |
| Judge0 self-hosted | Custom container runner | Judge0 (open-source, ISO 25010 security-hardened, per its IEEE paper) is the reference; self-building a sandbox is a high-risk custom security project |
| Judge0 | E2B / Vercel Sandbox / Modal | Hosted Firecracker microVM options — paid, evaluate when production costs matter |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Prisma `latest` (8.0.0-rc.12) today | Release candidate, not stable | Drizzle 0.45 or Prisma 7.10.0 stable |
| Executing student code via child_process on the app server | Any student code = full server compromise | Isolated sandbox service (containers/microVM), never on the web tier |
| Kubernetes for v1 | Premature for team size; 16 GB local dev machine | Docker Compose locally; defer k8s until scale demands it |
| Firebase/Supabase as primary store | Vendor lock-in on core education data; relational guarantees weaker | PostgreSQL you control (hosted anywhere later) |

## Stack Patterns by Variant

**If JS/TS track (v1 target):**
- Sandboxing can start with `node:vm`-free hardened containers (node:22-alpine + seccomp/no-network/limits) because languages match the app runtime
- Fastest path to interactive browser challenges (Monaco editor + postMessage iframe sandbox for HTML/CSS)

**If multi-language tracks (Python, Java, C, Go, Rust …):**
- Judge0-style execution service becomes mandatory (per-language images, compile+run phases)
- Do not grow a bespoke polyglot runner until Judge0 approach is exhausted

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| next@16 | react@19.2.x, eslint-config-next@16 | Match majors |
| tailwindcss@4 | @tailwindcss/postcss@4 | v4 is CSS-first; no tailwind.config required |
| typescript@7 | next@16 | Verify at scaffold; drop to 5.9.x if toolchain incompatibility appears |
| drizzle-orm@0.45 | drizzle-kit@0.31 | Keep kit ≤ orm minor pairing per docs |
| vitest@4 | Node ^20 / ^22 / ≥24 | Node 22.22.2 on this machine is fine |
| eslint@10 | eslint-config-next@16 | Flat config era |

## Sources

- npm registry dist-tags (live, 2026-09-02): next, react, tailwindcss, typescript, prisma, drizzle-orm, drizzle-kit, next-auth, vitest, eslint, @playwright/test, zod — HIGH confidence
- judge0.com and github.com/judge0/judge0 — open-source execution system, security claims per its IEEE/ISO 25010 paper — MEDIUM-HIGH
- 2026 sandbox comparisons (rustbox.sh, beam.cloud, modal.com, digitalapplied.com): E2B and Vercel Sandbox (GA Jan 2026) run Firecracker microVMs — MEDIUM
- Drizzle vs Prisma 2026 comparisons (makerkit.dev, zenstack.dev, vercel.com) — MEDIUM

---
*Stack research for: Code Journey — free coding education platform*
*Researched: 2026-09-02*
