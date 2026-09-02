# Environment (Audited 2026-09-02)

Read-only audit of the machine this foundation was built on, recorded so future
"works here" questions have a reference point.

## Machine

| Item                     | Value                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| OS                       | macOS 26.6.2 (arm64)                                                                       |
| CPU                      | Apple M4, 10 cores                                                                         |
| RAM                      | 16 GB                                                                                      |
| Node.js                  | 22.22.2                                                                                    |
| pnpm / npm / yarn / bun  | 10.4.0 / 10.9.7 / 1.22.22 / 1.3.12                                                         |
| Python                   | 3.9.6 (Apple Command Line Tools) — NOT used by this project                                |
| Git                      | 2.50.1                                                                                     |
| Docker / Compose         | 29.5.2 / v5.1.3 (daemon not running at audit time; Docker Desktop installed)               |
| PostgreSQL               | 16.13 client (Homebrew); **server not running** — project uses Docker instead from Phase 2 |
| Redis                    | not installed (not needed yet)                                                             |
| Browsers                 | Brave, Safari (Playwright downloads its own when E2E lands in Phase 6)                     |
| Other toolchains present | Go 1.26.1, Rust 1.95, Java 25, clang, GNU Make 3.81, Homebrew 6.x                          |

## Known Environment Quirks

- **Ports 3001 and 5173** were occupied by other processes at audit time. This project
  uses **3000** by default; alternative documented in README.
- **Docker daemon not auto-started.** Phase 2's `pnpm db:up` will need Docker Desktop
  running; the command should fail with a clear message if it is not.
- **No global git `user.name`** existed; repository-local identity was configured
  during init (`TysonTranThai` / `TysonTranThai@users.noreply.github.com`).
- `~/.gsd/defaults.json` sets global GSD keys that are ignored in favor of project
  config (harmless warning in GSD tooling).

## Environment Variables

Strategy: `.env.example` is the single source of truth for variable names (placeholders
only). Real values live in `.env.local`, which is git-ignored. **The foundation
requires no environment variables at runtime** — the variables below are declared for
the architecture documented in `docs/ARCHITECTURE.md` and are consumed by their
respective phases.

| Variable                                    | Purpose                                                                                         | Phase |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----- |
| `DATABASE_URL`                              | PostgreSQL connection (Docker Compose, port 5433 to avoid a common local 5432)                  | 2     |
| `AUTH_SECRET`                               | Session signing secret (`openssl rand -base64 32`)                                              | 2     |
| `AUTH_URL`                                  | Canonical app URL for auth callbacks                                                            | 2     |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth credentials                                                                        | 2     |
| `AI_API_KEY` / `AI_BASE_URL`                | AI mentor provider (provider-agnostic adapter; empty = features off, platform fully functional) | 5     |
| `EMAIL_FROM` / `SMTP_URL`                   | Email transport; when unset in dev, mail logs to console                                        | 2     |

Rules:

1. Only variables actually consumed by installed code belong in `.env.example`.
2. `NEXT_PUBLIC_*` variables must never contain secrets (they ship to browsers).
3. No real secret is ever committed; CI/service credentials live outside git.
