# Architecture Research

**Domain:** Coding education platform (online judge + LMS + community)
**Researched:** 2026-09-02
**Confidence:** MEDIUM-HIGH

## Standard Architecture

### System Overview

```
+------------------------------------------------------------------+
|                        Browser (learner)                          |
|   Next.js UI  --  Monaco editor  --  preview iframes (sandboxed)  |
+------------------------------+-----------------------------------+
                               | HTTPS
+------------------------------v-----------------------------------+
|                 Web app (Next.js modular monolith)                |
|  RSC pages | API routes / server actions | auth | progress | AI   |
+----------+-----------------------+---------------------+---------+
           |                       |                     |
           |                       v                     |
           |            +---------------------+          |
           |            | PostgreSQL (data)   |          |
           |            +---------------------+          |
           v                                             v
+-----------------------------+          +----------------------------+
| Code execution service      |          | AI provider (adapter)      |
| (Judge0-style containers /  |          | hints, explanations, review|
|  microVM; separate host in  |          | anti-solve guardrails      |
|  production; never app srv) |          +----------------------------+
+-----------------------------+
           |
           v
+-----------------------------+
| Background jobs (queue)     |
| grading, emails, analytics  |
+-----------------------------+
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Web app (Next.js) | UI, auth flows, content serving, submissions API | Next 16 App Router, RSC, server actions |
| Database | Users, curriculum, submissions, progress, discussions | PostgreSQL + Drizzle |
| Execution service | Run untrusted code in isolation, return tests verdict | Containers/microVM (Judge0-style), strict limits |
| Background jobs | Async grading, emails, rollups | Simple queue table + worker in monolith initially |
| AI service | Mentor features behind guardrails | Provider-agnostic adapter interface |
| Object storage | Project assets, submissions archive | Local FS in dev; S3-compatible later |

## Recommended Project Structure

```
src/                        # Next.js application (the monolith)
├── app/                    # App Router pages & API routes
│   ├── (marketing)/        # landing, about
│   ├── (learn)/            # dashboard, track/course/lesson pages
│   └── api/                # route handlers (submissions, ai, webhooks)
├── components/             # UI components
├── lib/                    # shared server code
│   ├── db/                 # drizzle schema + client
│   ├── auth/               # auth config
│   ├── execution/          # execution-service client + queue
│   ├── ai/                 # mentor adapter interface
│   └── curriculum/         # content loaders
├── content/                # curriculum content-as-data (MDX/JSON)
└── styles/

services/                   # future split-out services (stubs now)
└── execution/              # runner worker + containers (Phase later)

docs/                       # architecture, security, a11y, runbooks
```

### Structure Rationale

- **Monolith-first:** single deployable; module boundaries (`lib/*`) mark future service seams
- **content-as-data:** curriculum as MDX/JSON in repo → reviewable, free hosting, git-native contributions
- **services/execution:** the one subsystem with a security-driven reason to be isolated from day 1 (in production it runs on separate infrastructure with no DB credentials)

## Architectural Patterns

### Pattern 1: Modular monolith with service seams

**What:** One Next.js app; internal modules with explicit boundaries; execution service isolated early
**When to use:** Team ≤ 5, uncertain which parts need scaling
**Trade-offs:** Simpler ops vs. eventual extraction effort

### Pattern 2: Content-as-data (git-native curriculum)

**What:** Lessons/challenges in repo as MDX/JSON, loaded at build or via ISR
**When to use:** Free platform, community PRs, versioned curriculum
**Trade-offs:** Content changes require deploys; caching strategy needed

### Pattern 3: Execution via isolated job queue

**What:** Submission → queue row → runner worker picks up → executes in container → writes verdict
**When to use:** Any auto-graded challenge; decouples web latency from execution latency
**Trade-offs:** Polling/websocket UX complexity; queue infra needed (start with Postgres-backed queue)

### Pattern 4: Provider-agnostic AI adapter with pedagogical guardrails

**What:** `MentorAdapter` interface (hint/explain/review) implemented by any LLM provider; system prompts enforce "never provide full solutions"
**When to use:** From first AI feature
**Trade-offs:** Slightly more abstraction than hardcoding one provider

## Data Flow

### Request Flow (submission grading)

```
Student submits code
    → API route validates (zod) + persists submission
    → enqueues execution job (Postgres-backed queue row)
    → runner worker claims job, dispatches to sandbox container
    → container runs code against challenge tests (timeouts, limits)
    → verdict + logs written back; progress updated
    → UI shows pass/fail with test output
```

### Key Data Flows

1. **Lesson flow:** content file → parsed → RSC render → completion event → progress row
2. **AI flow:** student request → guardrail check (anti-cheat prompt + rate limit) → adapter → provider → streamed hint

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k users | Monolith + Postgres + single worker; zero premature optimization |
| 1k-100k users | Execution service on separate hosts; Redis for queue/rate limits; CDN for content |
| 100k+ users | MicroVM pool (Firecracker), read replicas, regional execution clusters |

### Scaling Priorities

1. **First bottleneck: code execution concurrency** — it's CPU-bound and security-bound; design the queue for horizontal workers now (execution lives behind an interface so the transport can change)
2. **Second bottleneck: AI costs** — rate limiting + caching + small-model routing

## Anti-Patterns

### Anti-Pattern 1: Student code on the app server

**What people do:** `child_process`/`eval` on the Next.js server "for now"
**Why it's wrong:** Any submission = remote code execution against the platform
**Do this instead:** Isolated runner from the very first graded challenge

### Anti-Pattern 2: Browser-only eval grading

**What people do:** Evaluate student answers with `eval` in the browser for simplicity
**Why it's wrong:** Trivially bypassable; teaches wrong patterns
**Do this instead:** Same test-harness + verdict model as server grading

### Anti-Pattern 3: Curriculum hardcoded in React components

**What people do:** Lessons as JSX components
**Why it's wrong:** Unreviewable at scale; no contribution path
**Do this instead:** Content-as-data with schema validation (zod) at load

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| LLM provider | Adapter interface (`MentorAdapter`) | Key held in env; never exposed client-side |
| Email (verification/reset) | Pluggable mailer interface; dev = log transport | Choose SMTP/Resend/Postmark at implementation |
| GitHub OAuth | Auth.js provider config | Also future project-submission integration |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| web ↔ execution | Job queue rows + verdict callbacks | Web never touches sandbox directly |
| web ↔ AI | Server-side adapter only | Rate limits per user |
| content → web | Build-time load + zod validation | Fails build on invalid content |

## Sources

- Judge0 architecture paper & docs — MEDIUM-HIGH
- freeCodeCamp/Exercism public architecture discussions — MEDIUM
- Next.js 16 App Router documentation — HIGH

---
*Architecture research for: Code Journey — free coding education platform*
*Researched: 2026-09-02*
