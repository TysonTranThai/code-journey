# Project Research Summary

**Project:** Code Journey — free coding education platform
**Domain:** Online judge + LMS + community
**Researched:** 2026-09-02
**Confidence:** HIGH (stack versions verified live; domain patterns multi-sourced)

## Executive Summary

Code Journey belongs to a well-understood product family: a structured curriculum (LMS), an interactive challenge loop (online judge), and a community layer. Experts build this as a **modular monolith with one hard isolation boundary — the code execution service** — because that's the only subsystem where untrusted input is *executed*, making it the platform's defining security constraint. The recommended stack is Next.js 16 (App Router, React 19) + TypeScript 7 + Tailwind 4 with PostgreSQL via Drizzle ORM, Vitest/Playwright for tests. Curriculum should live as **content-as-data** (MDX/JSON in-repo, zod-validated) to enable free, git-native contribution. The AI mentor is a differentiating feature but must be **pedagogy-first**: an adapter interface with anti-solve guardrails, not a raw LLM chat.

The main risks concentrate in two places: sandbox security (mitigate by adopting Judge0-style hardening checklists and never running student code on the web tier) and curriculum scale (mitigate by content-as-data from lesson one). Everything else is conventional web engineering.

## Key Findings

### Recommended Stack

Next.js 16.3.4 + React 19.2.8 + TypeScript 7.0.2 + Tailwind 4.3.3, PostgreSQL via Drizzle ORM 0.45, Zod 4, ESLint 10 flat config, Vitest 4 + Playwright 1.62. pnpm as package manager. Auth.js (NextAuth v5 line) as the authentication pattern — exact package/version decided at auth implementation phase.

**Core technologies:**
- Next.js 16 — web app + API in one modular monolith
- PostgreSQL 16 + Drizzle — relational core with TS-native schema
- Vitest 4 + Playwright 1.62 — every subsystem testable from day one
- Docker Compose — local Postgres now, sandbox prototyping later

### Expected Features

**Must have (table stakes):** auth, curriculum browser, interactive auto-graded challenges, progress tracking, browser code editor, responsive lessons
**Should have (competitive):** pedagogy-first AI mentor, WCAG 2.1 AA accessibility, multi-language tracks later, community discussions
**Defer (v2+):** full browser IDE, mobile apps, classroom mode, multi-language sandbox expansion

### Architecture Approach

Modular monolith (Next.js) with explicit module seams (lib/db, lib/auth, lib/execution, lib/ai) and a separate execution runner designed for isolation from day one. Postgres-backed job queue first; Redis only when needed. Content-as-data curriculum. Provider-agnostic AI adapter with guardrails.

**Major components:**
1. Web app (Next.js) — UI, auth, content, submissions API
2. PostgreSQL — single source of truth
3. Execution service — isolated untrusted-code runner (never on web tier)
4. AI adapter — guarded mentor features
5. Background jobs — grading, emails

### Critical Pitfalls

1. **Student code on the app server** — never; queue → isolated runner from the first graded challenge
2. **Sandbox that works but isn't secure** — enforce per-run: no network, FS isolation, CPU/mem/PID limits, timeouts, non-root; audit before launch
3. **Hardcoded curriculum** — content-as-data with zod validation, build fails on invalid content
4. **Client-trusted progress** — server-verified completion events only
5. **AI mentor auto-solving** — hint ladders, refusal tests for "just solve it"

## Implications for Roadmap

### Phase 1: Foundation & Verification
**Rationale:** Everything depends on a trustworthy, reproducible dev environment
**Delivers:** Scaffolded Next.js/TS/Tailwind app, pnpm scripts (dev/build/lint/typecheck/test), ESLint+Prettier, Vitest, git hygiene (.gitignore, secrets policy), README/docs skeleton, health check green
**Addresses:** Infrastructure table stakes; avoids "works on my machine"
**Avoids:** Foundation drift; unverified tooling claims

### Phase 2: Data, Auth & Content Pipeline
**Rationale:** Identity + data model + content pipeline unblock every feature
**Delivers:** Postgres via Docker Compose, Drizzle schema for users/progress core, Auth.js email+GitHub (dev posture), .env.example, content loader with zod schema + sample content, db scripts (db:migrate, db:seed)
**Addresses:** Auth + curriculum content table stakes
**Avoids:** Auth bolted on late; hardcoded content

### Phase 3: Challenge Loop & Sandbox Execution
**Rationale:** The core product loop and the highest-risk subsystem
**Delivers:** Postgres-backed job queue, runner worker + containerized Node sandbox (no-network, limits, timeouts), submission API, Monaco editor challenge page, verdict UX, malicious-sample security tests
**Addresses:** The defining feature; sandbox hardening pitfall
**Avoids:** Student code on web tier

### Phase 4: Progress, Community & AI Mentor
**Rationale:** Retention and differentiation, after the core loop works
**Delivers:** Server-verified progress + streaks/achievements, discussions anchored to content, AI mentor adapter (hint/explain modes, guardrails + rate limits), optional provider via env
**Addresses:** Progress model + AI philosophy pitfalls
**Avoids:** Client-trusted progress; AI auto-solving

### Phase 5: Hardening, A11y & Launch Prep
**Rationale:** Public-quality bar before real users
**Delivers:** WCAG 2.1 AA pass, performance budget, observability (logs/errors/metrics), security review, E2E suite, deployment path decision
**Addresses:** Accessibility + security claims made only after verification
**Avoids:** Launching on unverified claims

### Phase Ordering Rationale

- Execution sandbox deliberately lands **after** data/auth but **before** progress/AI, because grading events feed both
- Content pipeline precedes challenge content needs
- A11y and security review are phases, not afterthoughts, because retrofits cost more

### Research Flags

- **Phase 3 (sandbox):** needs deeper research at planning time — isolation tech choice (Docker hardening vs gVisor vs Firecracker vs self-hosted Judge0) depends on deployment target
- **Phase 4 (AI):** provider choice intentionally open; adapter keeps it swappable

Phases with standard patterns (skip research-phase):
- Phase 1, 2, 5 — well-documented, established patterns

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Versions verified live from npm registry on 2026-09-02 |
| Features | MEDIUM-HIGH | Multi-competitor analysis |
| Architecture | MEDIUM-HIGH | Judge0/freeCodeCamp prior art |
| Pitfalls | MEDIUM-HIGH | Domain-specific, phase-mapped |

**Overall confidence:** HIGH

### Gaps to Address

- **Auth.js v5 (next-auth beta) exact version** — verify at implementation; fallback documented in STACK.md
- **Isolation tech choice** — open until deployment target is known (Phase 3 flag)
- **AI provider** — intentionally undecided; adapter interface first

## Sources

### Primary (HIGH confidence)
- npm registry dist-tags (live queries, 2026-09-02): next 16.3.4, react 19.2.8, typescript 7.0.2, tailwindcss 4.3.3, drizzle-orm 0.45.2, drizzle-kit 0.31.10, vitest 4.1.11, eslint 10.9.1, @playwright/test 1.62.1, zod 4.5.4, next-auth 4.24.15, prisma dist-tags (latest=8.0.0-rc.12, prev/stable=7.10.0)

### Secondary (MEDIUM-HIGH)
- judge0.com / github.com/judge0/judge0 — sandbox hardening reference
- 2026 sandbox landscape: E2B & Vercel Sandbox (GA Jan 2026) use Firecracker microVMs

### Tertiary (MEDIUM)
- Drizzle vs Prisma 2026 comparisons (makerkit.dev, zenstack.dev, vercel.com)
- freeCodeCamp/Exercism/Codecademy product analysis

---
*Research completed: 2026-09-02*
*Ready for roadmap: yes*
