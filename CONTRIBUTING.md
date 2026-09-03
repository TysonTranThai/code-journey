# Contributing to Code Journey

Thank you for helping build free coding education. This document covers the basics;
workflow details will grow as the project does.

## Development Setup

```bash
git clone <repo-url>
cd code-journey
pnpm install
pnpm dev
```

Verify your environment: <http://localhost:3000/health> should return `{"status":"ok"}`.

## Ground Rules

1. **Never commit secrets.** Real credentials go in `.env.local` (git-ignored).
   `.env.example` carries placeholders only.
2. **Never execute untrusted code on the web tier.** Student code runs only in the
   sandboxed execution service (see `docs/SECURITY.md`).
3. **Strict typing.** New code must pass `pnpm typecheck` (strict TypeScript) with no
   `any` unless justified in review.
4. **Accessible by default.** Semantic HTML, keyboard support, visible focus states.
   See `docs/ACCESSIBILITY.md`.

## Quality Gates

Run before every commit (all three must pass):

```bash
pnpm lint
pnpm typecheck
pnpm test
```

Formatting is enforced via `pnpm format:check` (Prettier). Run `pnpm format` to fix.

For changes touching the challenge loop, also run `pnpm test:e2e` (Playwright +
axe-core AA audits; needs Docker) and keep the sandbox isolation suite green
(`pnpm test -- sandbox-isolation`).

## Dependency Policy

- Adding a dependency requires justification in the PR description (why, and why the
  maintained alternative was rejected).
- `pnpm audit` must stay clean or carry a documented exception in
  [`docs/SECURITY.md`](docs/SECURITY.md) (never a silent ignore).

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) style:
`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`.

## Branching

- `main` — always green (lint + typecheck + tests pass)
- Feature branches: `feat/<short-name>`, `fix/<short-name>`

## Project Management

Planning docs (project context, requirements, roadmap) live in `.planning/` and are
managed via the GSD workflow. Roadmap phases map to requirements in
`.planning/REQUIREMENTS.md`.
