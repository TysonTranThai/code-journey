# Code Journey

> Learn to code. Free, forever.

A free, next-generation coding education platform: structured curriculum, interactive
auto-graded challenges executed in an isolated sandbox, progress tracking, community,
and an AI coding mentor that teaches instead of solving.

**Development status:** v0.1.0 — curriculum browsing, accounts (email), auto-graded
challenge loop with sandbox execution, learner dashboard with verified progress +
achievements, lesson discussions, and the mentor foundation (hints + guardrails, no
provider selected) are implemented. See [`.planning/ROADMAP.md`](.planning/ROADMAP.md)
for what ships next.

## Prerequisites

| Tool           | Version    | Notes                                                      |
| -------------- | ---------- | ---------------------------------------------------------- |
| Node.js        | ≥ 22       | Developed on 22.22.2                                       |
| pnpm           | 10.x       | Developed on 10.4.0 (`corepack enable` or `npm i -g pnpm`) |
| Docker Desktop | any recent | PostgreSQL + the sandbox image (unit tests run without it) |
| Git            | ≥ 2.40     |                                                            |

## Quick Start

```bash
pnpm install        # install dependencies
pnpm db:up          # start Postgres via Docker Compose (localhost:5433)
pnpm db:migrate     # apply Drizzle migrations
pnpm db:seed        # insert dev identity fixtures (dev-student / dev-admin)
pnpm dev            # start dev server at http://localhost:3000
```

Health check: open <http://localhost:3000/health> — expect `{"status":"ok","db":"up"}`.

> **Port note:** if port 3000 is taken on your machine, run `pnpm dev -- -p 3100`
> (ports 3001 and 5173 are commonly occupied by other tools).

## Commands

All commands verified working as of 2026-09-02:

| Command              | What it does                                                        |
| -------------------- | ------------------------------------------------------------------- |
| `pnpm dev`           | Start the Next.js dev server on port 3000                           |
| `pnpm build`         | Production build (includes type checking)                           |
| `pnpm start`         | Serve the production build                                          |
| `pnpm lint`          | ESLint (flat config, Next.js core-web-vitals + TypeScript)          |
| `pnpm lint:fix`      | ESLint with auto-fix                                                |
| `pnpm format`        | Format all files with Prettier                                      |
| `pnpm format:check`  | Verify formatting without writing                                   |
| `pnpm typecheck`     | TypeScript strict check (`tsc --noEmit`)                            |
| `pnpm test`          | Unit + integration tests (Vitest; DB-dependent suites auto-skip)    |
| `pnpm test:watch`    | Vitest in watch mode                                                |
| `pnpm test:e2e`      | Playwright E2E incl. axe-core AA audits (needs Docker for the loop) |
| `pnpm worker`        | Challenge runner worker — the only process that executes code       |
| `pnpm sandbox:build` | Build the hardened sandbox image (required for the challenge loop)  |
| `pnpm db:up`         | Start Postgres via Docker Compose                                   |
| `pnpm db:down`       | Stop the Postgres container (data volume kept)                      |
| `pnpm db:migrate`    | Apply Drizzle migrations                                            |
| `pnpm db:seed`       | Insert dev identity fixtures (local passwords only)                 |
| `pnpm db:reset`      | Drop volume, recreate, migrate, seed (clean slate)                  |
| `pnpm db:generate`   | Generate a migration from schema changes (drizzle-kit)              |
| `pnpm db:studio`     | Drizzle Studio (browse data)                                        |

## Running the Challenge Loop Locally

The sandbox executes student code in a locked-down container — never on the web tier:

```bash
pnpm db:up
pnpm db:migrate
pnpm sandbox:build   # once; rebuild after changing docker/Dockerfile.sandbox
pnpm worker          # terminal 1: polls the execution queue
pnpm dev             # terminal 2: the app
```

Open a challenge (e.g. learn → Web Development → HTML Foundations → a lesson →
a practice challenge), edit the code, press **Run code**, and see the verdict.
With no worker running, submissions stay queued and the UI says so.

## Database

PostgreSQL 16 runs via Docker Compose (no native install needed). Copy `.env.example`
to `.env.local` first — `DATABASE_URL` points at `localhost:5433`. The seed creates
**local development fixtures only** (password `dev-password-123`), never real accounts.
`pnpm test` includes DB integration tests that **skip automatically** when the
database is down.

## Architecture (summary)

Modular monolith: one Next.js application (UI + API), PostgreSQL as the single source
of truth, curriculum content as version-controlled data (JSON + MDX, validated at load
— invalid content fails the build), and one hard security boundary — **student code
never executes on the web tier**; it runs only in an isolated sandbox behind a job
queue, driven by a separate worker process.

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — components, boundaries, data flow
- [`docs/DATA-MODEL.md`](docs/DATA-MODEL.md) — conceptual schema and relationships
- [`docs/SECURITY.md`](docs/SECURITY.md) — security posture: implemented / planned / not-yet-verified
- [`docs/A11Y.md`](docs/A11Y.md) — WCAG 2.1 AA statement: what is verified, known gaps
- [`docs/ACCESSIBILITY.md`](docs/ACCESSIBILITY.md) — accessibility requirements & conventions
- [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md) — audited dev machine + environment variables

## Environment Variables

Copy `.env.example` to `.env.local` and fill values as needed. Required today:
`DATABASE_URL` (Docker Postgres) and `AUTH_SECRET` (generate with
`openssl rand -base64 32`). OAuth/AI-provider keys stay placeholders until those
integrations are selected. Never commit real secrets (`.env*` is git-ignored except
`.env.example`).

## Project Structure

```
src/
├── app/                # App Router pages & route handlers
├── components/         # UI components (learn, challenge, discussion, layout…)
├── content/            # Curriculum as data: tracks → courses → modules → lessons
│                       #   (+ challenges per lesson, achievements.json)
├── lib/                # Server/shared code (db, curriculum, execution, mentor…)
├── server/             # Auth config, guards, server actions
└── workers/            # Runner worker + sandbox execution (never imported by the web tier)
tests/
├── unit/               # Vitest unit tests (no DB required)
├── integration/        # DB/queue/sandbox suites (auto-skip without Docker)
└── e2e/                # Playwright: critical path, anonymous, accessibility
docs/                   # Architecture, security, a11y, data model, environment
.planning/              # GSD workflow: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, research/
```

## Tech Stack

Next.js 16 (App Router) · React 19 · TypeScript 6 (strict) · Tailwind CSS 4 ·
Drizzle ORM + PostgreSQL 16 · Auth.js (credentials; OAuth ready) · Zod 4 ·
Monaco editor · MDX · ESLint 9 (flat config) + Prettier · Vitest 4 · Playwright ·
Docker (Postgres + hardened sandbox).
Version rationale and alternatives: [`.planning/research/STACK.md`](.planning/research/STACK.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Every change must keep
`pnpm lint`, `pnpm typecheck`, and `pnpm test` green.

## License

TBD before first public release (an OSI license will be chosen; the mission is free education).
