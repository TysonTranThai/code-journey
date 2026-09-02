# Code Journey

## What This Is

Code Journey is a free, next-generation coding education platform — a modern alternative to FreeCodeCamp. It will combine a structured curriculum, interactive coding challenges, a browser-based development environment, automatic test-verified submissions, progress tracking, community features, and an optional AI coding mentor that helps students learn rather than doing the work for them.

## Core Value

A student can go from zero to job-ready developer skills entirely for free: learn a concept in structured lessons, practice it in interactive challenges, have their code automatically executed and verified in a sandbox, and see real progress — with an AI mentor that teaches instead of just giving answers.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Structured curriculum (foundations → web → backend → full stack → advanced → specializations)
- [ ] Interactive coding challenges with automatic test-verified execution
- [ ] Browser-based code editor / development environment
- [ ] User accounts, authentication, profiles, and progress tracking
- [ ] Achievements and streaks
- [ ] Community discussions (forums/comments on lessons and challenges)
- [ ] Optional AI coding mentor (hints, explanations, code review — never auto-solving)
- [ ] Sandboxed code execution service (multi-language)
- [ ] Projects with submission and review
- [ ] Analytics and observability

### Out of Scope

- Paid tiers / paywalled content — the mission is free education for everyone
- Mobile native apps — responsive web first
- Live 1:1 tutoring marketplace — different product category
- Production Kubernetes deployment at this stage — scale infrastructure only when needed

## Context

- Greenfield project initialized September 2026 in an empty git repo at `/Users/tysontran/Documents/Code Journey`; only a `.freebuff/project-id` marker existed.
- Development machine: macOS 26.6.2, Apple M4, 16 GB RAM. Node 22.22.2, pnpm 10.4.0, Docker 29.5.2 (daemon not always running), PostgreSQL 16 client installed (server not running). No global git user.name was configured; repo-local identity was set during init.
- Ports 3001 and 5173 are occupied by other processes on the dev machine; the dev server will use a different port.
- The platform will eventually support executing code in many languages (JavaScript, TypeScript, Python, HTML/CSS, SQL, Java, C, C++, Go, Rust) inside an isolated sandbox. This is the highest-risk subsystem and will be designed defensively (containers/microVMs, resource limits, network isolation) but never trusted prematurely.
- The AI mentor's educational philosophy: explain, hint, review, debug — never complete assignments for the student. Provider-agnostic by design.

## Constraints

- **Tech stack**: TypeScript-first (Next.js App Router + Tailwind for the web app), pnpm as package manager — chosen for developer velocity and type safety across the whole platform
- **Cost**: Free for learners; minimize infrastructure cost — no paid services required during development
- **Security**: Arbitrary student code must never execute on the main application server or with access to platform secrets
- **Accessibility**: WCAG 2.1 AA is a product requirement, not an afterthought
- **Simplicity**: Modular monolith first; no premature microservices or Kubernetes

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Greenfield from empty repo | Workspace contained no existing code | — Pending |
| Next.js full-stack modular monolith | Single deployable, fastest path to working product, matches team size of 1 | — Pending |
| pnpm as package manager | v10.4.0 installed; fast, strict, good workspace story for future service split | — Pending |
| PostgreSQL as primary database | Relational data (users, progress, submissions) fits it well; installed locally via Homebrew | — Pending |
| Docker for local infra + sandbox prototyping | Docker Desktop installed; sandbox isolation is a hard requirement later | — Pending |
| AI mentor is provider-agnostic, pedagogy-first | Educational value > convenience; interface defined before provider choice | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-02 after initialization*
