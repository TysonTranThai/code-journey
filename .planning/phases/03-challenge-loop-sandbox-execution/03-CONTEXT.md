# Phase 3: Challenge Loop & Sandbox Execution - Context

**Gathered:** 2026-09-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 delivers the platform's defining loop: a student writes code in the browser, submits it, and receives test-by-test verdicts produced by an isolated sandbox. This includes the Postgres-backed execution queue, the hardened container runner, the challenge content model, the submissions API, and the challenge UI. Progress recording (PROG), achievements, AI mentor, and community are later phases. Standing constraint: student code NEVER executes on the web tier; the browser never executes student code with platform privileges (PLAT-08).

</domain>

<decisions>
## Implementation Decisions

### Isolation technology
- **D-01:** Hardened Docker containers (OWASP Docker Security Cheat Sheet baseline) — verified approach for the v1 JS/TS track where the sandbox runtime matches the app runtime. Judge0 self-hosted / Firecracker microVMs / hosted sandboxes (E2B, Vercel Sandbox) remain the documented production-evolution paths; re-evaluate when a deployment target exists. **No claim of execution security is made until the malicious-sample suite passes — that suite is the phase's hard gate.**
- **D-02:** Sandbox image `node:22-alpine` (pinned locally via a small Dockerfile, NOT `latest`), executed with: `--network none`, `--read-only` rootfs + `--tmpfs /tmp:size=16m`, `--memory 256m`, `--cpus 0.5`, `--pids-limit 64`, `--cap-drop ALL`, `--security-opt no-new-privileges`, non-root user, wall-clock timeout (10s) enforced by the runner (docker stop + SIGKILL).

### Architecture
- **D-03:** Postgres-backed queue: `execution_jobs` table (status: queued → claimed → running → completed/failed; claimedBy, claimedAt, attempts). Workers claim via `SELECT … FOR UPDATE SKIP LOCKED` — safe for multiple workers, no extra queue infra.
- **D-04:** Runner worker = separate Node process (`src/workers/runner.ts`, started with `pnpm worker`, tsx). It — and only it — talks to the Docker CLI (`docker run`, per-job container). The web tier never spawns interpreters (anti-pattern 1 in research). Production note in code: worker moves to a separate host with its own Docker socket and no DATABASE_URL-for-users credentials.
- **D-05:** Verdict flow: API validates + inserts submission & job → worker claims job → writes student code + tests into tmpfs → runs container → parses per-test results → writes verdict → UI polls submission. Verdict states and payloads are typed and shared (`src/lib/execution/types.ts`).

### Challenge content model
- **D-06:** Extends the curriculum content-as-data system: `challengeSchema` (id, title, prompt, difficulty, boilerplate, tests: array of { name, code } assertion snippets with educational failure hints). Challenges live next to lessons (`…/lessons/<lessonId>/challenges/<challengeId>.json`), validated with zod + cross-reference (lesson.challenges ids must resolve). Seed: 2 challenges on HTML Foundations lessons (fix the broken heading; add the missing link) with real test code.
- **D-07:** Submissions are immutable snapshots (docs/DATA-MODEL.md principle 3): `submissions` table (userId, challengeId, code, verdict, perTestResults jsonb, runtimeMs, createdAt; no updates). Anonymous users can RUN code (rate-limited); only logged-in users can SUBMIT for recording (CHAL-03).
- **D-08:** Draft persistence (CHAL-06) = localStorage keyed by challenge id (client-only, survives refresh). Server-side drafts deferred — not required by the roadmap criterion.

### UI (WEB-ONLY / PLAT-06)
- **D-09:** Challenge route under its lesson: `/learn/[trackId]/[courseId]/[moduleId]/[lessonId]/challenge/[challengeId]` — preserves breadcrumbs and curriculum context.
- **D-10:** Responsive workspace: desktop = side-by-side (editor | instructions + output); mobile = intentional tab switcher (Instructions / Code / Output), not a shrunken desktop. Monaco via @monaco-editor/react (verify exact version at execution). Run + Submit buttons; verdict panel lists per-test pass/fail with educational messages; timeout state says "your code took too long — check for infinite loops".

### the agent's Discretion
- Exact test-harness protocol inside the container (node:test vs plain assertion script) as long as verdicts map to the typed result shape
- Monaco loading strategy (npm vs CDN loader)
- Poll interval / optimistic UI details

</decisions>

<specifics>
## Specific Ideas

- The malicious-sample isolation suite is a first-class deliverable, not an afterthought: fork bomb, network egress attempt, filesystem escape attempt, infinite loop, memory bomb — every sample must be contained or time out, asserted in `tests/integration/sandbox-isolation.test.ts` (Docker-gated, skipped when Docker is down).
- Educational failure output follows the CHAL-05 wording: show which test failed and why, never a bare boolean.
- The runner must redact/limit output (truncate stdout/stderr, no env leakage into job payload).

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Data + architecture
- `docs/DATA-MODEL.md` — ExecutionJob, Submission, TestCase entities and immutable-snapshot principle
- `docs/SECURITY.md` — sandbox hardening checklist and "not yet verified" honesty requirements
- `.planning/research/ARCHITECTURE.md` — execution flow (queue → runner → verdict), anti-patterns 1 & 2

### Constraints + requirements
- `.planning/REQUIREMENTS.md` — CHAL-01…06, PLAT-08 definitions
- `.planning/ROADMAP.md` — Phase 3 success criteria (incl. malicious-sample suite gate)
- `AGENTS.md` — web-only product constraint

### Prior-phase decisions
- `.planning/phases/02-data-auth-content-pipeline/02-CONTEXT.md` — D-09 (progress_events, do not implement yet), D-13 (content-as-data), auth/guards to reuse

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/lib/db/*` — client, schema (add execution_jobs + submissions here), migrations flow
- `src/lib/curriculum/loaders.ts` + `schema.ts` — extend for challenges; keep global-id uniqueness
- `src/lib/auth/guards.ts` — requireUser() for submissions
- `src/server/actions/auth.ts` — zod-validation + typed form-state pattern for the challenge actions
- `docker-compose.yml` — Docker Desktop already required; add the sandbox image build here or a sibling Dockerfile

### Established Patterns
- Zod at every trust boundary; server-only modules; tests that skip when infra is down (DB) — same for Docker
- Vitest alias `@/`; prettier + eslint gates before every commit

### Integration Points
- Lesson page (`…/[lessonId]/page.tsx`) links to its challenges once content exists
- `pnpm` scripts get `worker` (and `sandbox:build`)

</code_context>

<deferred>
## Deferred Ideas

- progress_events writes on passing submissions — Phase 4 (representation already locked)
- Multi-language sandboxes (Python/SQL/compiled) — v2 (EXEC-01…03)
- Redis/queue infra — only if Postgres queue shows real limits
- Server-side draft storage, full rate-limiting/abuse prevention — Phase 6 hardening
- Monaco/verdict UI polish beyond accessibility basics — Phase 6 a11y pass

</deferred>

---

*Phase: 03-challenge-loop-sandbox-execution*
*Context gathered: 2026-09-02*
