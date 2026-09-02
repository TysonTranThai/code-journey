# Phase 5: Community & AI Mentor - Context

**Gathered:** 2026-09-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 adds social learning (lesson-anchored discussions: post, reply, visitor read access) and the pedagogy-first AI mentor (graduated hints, error explanation, refusal tests, per-user rate limiting, graceful no-key degradation). Progress/achievements are done; hardening/a11y/E2E are Phase 6. Standing constraints: WEB-ONLY product; AI is a server-side web API only (PLAT-08); mentor must teach, never solve (project core philosophy).

</domain>

<decisions>
## Implementation Decisions

### Discussions (COMM-01…03)
- **D-01:** `discussion_threads` (id, lessonId content-as-data id, userId FK, title, createdAt) + `comments` (id, threadId FK cascade, userId FK, body 1..4000, createdAt; no edits in v1 — delete-own is Phase 6 hardening). Public read (visitors), authenticated write.
- **D-02:** Thread pages under the lesson route (`…/lesson/[lessonId]/discussion`) with a thread list + threads at `…/discussion/[threadId]`. Visitors can read everything; posting/replying requires a session (server-enforced); UI shows sign-in prompts for anonymous users.
- **D-03:** Server actions with zod validation for post/reply; the action re-verifies session + lesson existence server-side (client never asserts). XSS-safe by React escaping (no dangerouslySetInnerHTML anywhere).
- **D-04:** Comment count + last activity ordering on the thread list; content IDs validated against loaders so threads can only anchor to real lessons.

### Mentor architecture (AI-01…04, PLAT-08)
- **D-05:** `MentorAdapter` interface (server-only): `hint(context, level 1..3)` and `explainError(context, failedTest, errorOutput)` returning `{ text, refused? }`. Provider-agnostic; NO provider is implemented until a key exists — the only built-in adapter is `NullMentor` (AI-04).
- **D-06:** `NullMentor` returns structured degradation: hint requests get the challenge's own educational hints (already content-as-data — real value without AI); error explanation gets static guidance + the failing test's hint. `mentorAvailable()` checks `MENTOR_API_KEY` presence so the UI hides mentor CTAs when absent (graceful degradation, platform fully functional).
- **D-07:** Guardrails are adapter-agnostic and enforced server-side BEFORE display: hint ladder (level 1 nudge → level 2 direction → level 3 near-miss, never final code), plus a post-processing refusal filter that rejects any response containing full-solution markers (complete `<html>`/full function matching the solution pattern). Refusal test suite runs the filter against adversarial samples.
- **D-08:** Rate limiting (AI-03): `mentor_requests` table (userId, kind, createdAt) — server-side counter, per-user limits (10 hints/day, 20 error-explains/day in v1). Anonymous users: mentor is unavailable (auth required), which doubles as abuse prevention. Rate-limit errors return a friendly retry message.
- **D-09:** Mentor UI lives on the challenge page (hint button w/ level progression + "explain my error" when a failed verdict exists) and is driven by client state; requests go through a server action → adapter → guardrails → rate limit.

</decisions>

<specifics>
## Specific Ideas

- Refusal test suite: feed the filter full-solution-looking strings (complete document, verbatim boilerplate+answer) and assert refusal; feed hints ("check the closing tag", "href goes in quotes") and assert pass.
- The hint ladder is content-independent: level text derives from the challenge's test hints so it works for every challenge without per-challenge AI prompts.
- Thread list shows "be the first to ask" empty state — community seeding matters for a new platform.
- Rate limiting tests use a fresh user and loop until the limit trips, asserting the friendly error.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Data + architecture
- `docs/DATA-MODEL.md` — DiscussionThread/Comment/MentorSession entities, principle 5 (auditable refusals)
- `.planning/research/ARCHITECTURE.md` — AI service boundary (server-side only)
- `src/lib/db/schema.ts` — existing tables/patterns

### Constraints + requirements
- `.planning/REQUIREMENTS.md` — COMM-01…03, AI-01…04
- `.planning/ROADMAP.md` — Phase 5 success criteria (incl. refusal test suite, no-key degradation)
- `AGENTS.md` — web-only constraint; mentor-teaches philosophy

### Prior-phase decisions
- Phase 2 CONTEXT — content-as-data, server actions, guards
- Phase 4 — rate-limit table pattern precedent (none yet: this phase adds the first)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `requireUser()` guards; server action + zod pattern from `src/server/actions/auth.ts`
- Challenge verdict model (`PerTestResult.message`) — mentor error-explanation context
- Content loaders — lesson existence checks for thread anchoring
- Lesson page structure for embedding the discussion section

### Established Patterns
- DB-gated integration tests that skip cleanly; zod at boundaries; react-compiler-clean client components

### Integration Points
- Challenge page (ChallengeWorkspace) — mentor buttons next to Run
- Lesson page — discussion section link
- sitemap: threads are user-generated → keep out of sitemap (privacy/no-index strategy matches dashboard)

</code_context>

<deferred>
## Deferred Ideas

- Comment editing/deletion (own-content moderation) — Phase 6
- Voting/reactions, mentions — post-MVP
- Real AI provider (Anthropic/OpenAI/local) — when a key is provisioned; adapter + guardrails are ready
- Markdown rendering in comments — v1 is plain text (XSS-safest)
- Mentor conversation history persistence (MentorSession entities) — v1 is stateless requests; DATA-MODEL entities arrive with a real provider

</deferred>

---

*Phase: 05-community-ai-mentor*
*Context gathered: 2026-09-02*
