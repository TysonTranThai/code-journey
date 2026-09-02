# Architecture

**Status:** Foundation established 2026-09-02. Components marked PLANNED are designed
but not yet implemented; the roadmap phases that deliver them are referenced.

## System Overview

```
+------------------------------------------------------------------+
|                        Browser (learner)                          |
|   Next.js UI  --  code editor  --  preview iframes (sandboxed)    |
+------------------------------+-----------------------------------+
                               | HTTPS
+------------------------------v-----------------------------------+
|            Web app — Next.js (modular monolith)                   |
|  RSC pages | route handlers/server actions | auth | progress      |
+----------+-----------------------+---------------------+---------+
           |                       |                     |
           |                       v                     |
           |            +---------------------+          |
           |            | PostgreSQL 16       |          |
           |            | (Drizzle ORM)       |          |
           |            +---------------------+          |
           v                                             v
+-----------------------------+          +----------------------------+
| Code execution service      |          | AI provider (via adapter)  |
| PLANNED (Phase 3)           |          | PLANNED (Phase 5)          |
| isolated containers/microVM |          | pedagogy-first guardrails  |
| NEVER on the web tier       |          | provider-agnostic          |
+-----------------------------+          +----------------------------+
```

## Component Boundaries

| Component            | Responsibility                                         | Status                          |
| -------------------- | ------------------------------------------------------ | ------------------------------- |
| Web app (Next.js)    | UI, auth flows, content serving, submissions API       | IMPLEMENTED (scaffold)          |
| PostgreSQL + Drizzle | Users, curriculum, submissions, progress, discussions  | PLANNED — Phase 2               |
| Execution service    | Run untrusted code in isolation; verdicts              | PLANNED — Phase 3               |
| Job queue            | Async grading (Postgres-backed queue rows first)       | PLANNED — Phase 3               |
| AI adapter           | Mentor features behind pedagogical guardrails          | PLANNED — Phase 5               |
| Object storage       | Project assets, submission archives                    | PLANNED — local FS in dev first |
| Email                | Verification/reset mail; dev transport logs to console | PLANNED — Phase 2               |

## Module Seams (in-repo layout)

The monolith is organized so future service extraction is a deployment change, not a
rewrite:

```
src/lib/db/          # database schema + client        → Phase 2
src/lib/auth/        # authentication                  → Phase 2
src/lib/curriculum/  # content-as-data loaders         → Phase 2
src/lib/execution/   # queue + runner client           → Phase 3
src/lib/ai/          # MentorAdapter interface         → Phase 5
```

Rules:

- Modules communicate through explicit interfaces, not by reaching into each other's
  internals.
- The web tier never imports sandbox/runtime internals — only the queue client.
- Content is data (MDX/JSON validated with zod at build time), never JSX components.

## Submission Grading Flow (target)

```
Student submits code
  → API route validates (zod), persists submission row
  → enqueues execution job (queue row)
  → runner worker claims job, dispatches to sandbox container
  → container runs code against challenge tests (limits + timeouts enforced)
  → verdict + per-test results persisted; progress events recorded
  → UI renders per-test pass/fail with educational output
```

## Scaling Path (documented, not premature)

| Scale      | Adjustment                                                              |
| ---------- | ----------------------------------------------------------------------- |
| 0–1k users | Monolith + Postgres + single worker                                     |
| 1k–100k    | Execution service on separate hosts; Redis queue/cache; CDN for content |
| 100k+      | Firecracker-style microVM pool; read replicas; regional runners         |

The first expected bottleneck is code-execution concurrency (CPU-bound,
security-bound). The execution client is an interface from day one so the transport
(queue → dedicated service) can change without touching feature code.

## Decision Log (architecture-relevant)

| Decision                            | Rationale                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------- |
| Modular monolith, not microservices | Team of one; only execution has a security-driven isolation requirement today |
| Content-as-data (MDX/JSON + zod)    | Reviewable, git-native, free to host; build fails on invalid content          |
| Postgres-backed queue before Redis  | One less dependency; fine at v1 scale                                         |
| Provider-agnostic AI adapter        | No provider lock-in; guardrails and tests live in our code, not a vendor's    |
