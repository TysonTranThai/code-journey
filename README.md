# Code Journey

> Learn to code. Free, forever.

A free, next-generation coding education platform: structured curriculum, interactive
auto-graded challenges executed in an isolated sandbox, progress tracking, community,
and an AI coding mentor that teaches instead of solving.

**Development status:** Foundation phase (v0.1.0). The development environment, quality
gates, and architecture are established. Curriculum, challenges, auth, progress, and the
AI mentor ship in upcoming phases — see [`.planning/ROADMAP.md`](.planning/ROADMAP.md).

## Prerequisites

| Tool           | Version    | Notes                                                      |
| -------------- | ---------- | ---------------------------------------------------------- |
| Node.js        | ≥ 22       | Developed on 22.22.2                                       |
| pnpm           | 10.x       | Developed on 10.4.0 (`corepack enable` or `npm i -g pnpm`) |
| Docker Desktop | any recent | Needed from Phase 2 (PostgreSQL); not required yet         |
| Git            | ≥ 2.40     |                                                            |

## Quick Start

```bash
pnpm install        # install dependencies
pnpm dev            # start dev server at http://localhost:3000
```

Health check: open <http://localhost:3000/health> — expect `{"status":"ok",...}`.

> **Port note:** if port 3000 is taken on your machine, run `pnpm dev -- -p 3100`
> (ports 3001 and 5173 are commonly occupied by other tools).

## Commands

All commands verified working as of 2026-09-02:

| Command             | What it does                                               |
| ------------------- | ---------------------------------------------------------- |
| `pnpm dev`          | Start the Next.js dev server on port 3000                  |
| `pnpm build`        | Production build (includes type checking)                  |
| `pnpm start`        | Serve the production build                                 |
| `pnpm lint`         | ESLint (flat config, Next.js core-web-vitals + TypeScript) |
| `pnpm lint:fix`     | ESLint with auto-fix                                       |
| `pnpm format`       | Format all files with Prettier                             |
| `pnpm format:check` | Verify formatting without writing                          |
| `pnpm typecheck`    | TypeScript strict check (`tsc --noEmit`)                   |
| `pnpm test`         | Run unit tests (Vitest)                                    |
| `pnpm test:watch`   | Vitest in watch mode                                       |

Planned (added in their roadmap phases, not before): `pnpm db:up`, `pnpm db:migrate`,
`pnpm db:seed`, `pnpm test:e2e`.

## Architecture (summary)

Modular monolith: one Next.js application (UI + API) with explicit internal module
seams, PostgreSQL as the single source of truth, and one hard security boundary —
**student code never executes on the web tier**; it runs only in an isolated sandbox
service behind a job queue.

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — components, boundaries, data flow
- [`docs/DATA-MODEL.md`](docs/DATA-MODEL.md) — conceptual schema and relationships
- [`docs/SECURITY.md`](docs/SECURITY.md) — security posture: implemented / planned / not-yet-verified
- [`docs/ACCESSIBILITY.md`](docs/ACCESSIBILITY.md) — WCAG 2.1 AA requirements
- [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md) — audited dev machine + environment variables

## Environment Variables

Copy `.env.example` to `.env.local` and fill values as phases land.
**No environment variables are required to run the current foundation.**
Phase 1 declares the known upcoming variables with placeholders only —
never commit real secrets (`.env*` is git-ignored except `.env.example`).

## Project Structure

```
src/
├── app/                # App Router pages & route handlers
│   ├── layout.tsx      # Root layout (skip link, landmarks, metadata)
│   ├── page.tsx        # Landing page
│   └── health/route.ts # GET /health JSON status endpoint
├── lib/                # Shared server code (module seams for future services)
└── styles/             # (global styles live in src/app/globals.css)
tests/
└── unit/               # Vitest unit tests
docs/                   # Architecture, security, a11y, data model, environment
.planning/              # GSD workflow: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, research/
```

## Tech Stack

Next.js 16 (App Router) · React 19 · TypeScript 6 (strict) · Tailwind CSS 4 ·
Zod 4 · ESLint 9 (flat config) + Prettier · Vitest 4 · pnpm.
Version rationale and alternatives: [`.planning/research/STACK.md`](.planning/research/STACK.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Every change must keep
`pnpm lint`, `pnpm typecheck`, and `pnpm test` green.

## License

TBD before first public release (an OSI license will be chosen; the mission is free education).
