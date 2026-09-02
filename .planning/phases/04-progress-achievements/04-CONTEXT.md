# Phase 4: Progress & Achievements - Context

**Gathered:** 2026-09-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 4 turns grading events into progress a learner can see and trust: server-verified completion recording (lessons + challenges), a dashboard with overall progress and a consecutive-day streak, and server-side achievement awards for defined milestones. Community features and the AI mentor stay in Phase 5; hardening/polish in Phase 6. Standing constraints: progress writes are server-verified only (PROG-02, forged requests must fail); the product remains web-only with responsive UI (PLAT-06); private user pages (dashboard) must be no-index (PLAT-07).

</domain>

<decisions>
## Implementation Decisions

### Data model (locked in Phase 2, D-09: append-only progress_events)
- **D-01:** `progress_events` table (append-only): id, userId (FK cascade), contentType enum('lesson'|'challenge'), contentId (text — content-as-data id), createdAt. UNIQUE (userId, contentType, contentId) makes completion idempotent — re-completing is a no-op, and the unique constraint IS the source of truth for "done". No updated flags anywhere.
- **D-02:** `achievements` table: id, userId FK, achievementId text (slug of def), awardedAt. UNIQUE (userId, achievementId). Achievement *definitions* live as content-as-data JSON (`src/content/achievements.json`) with zod validation at load — same pipeline as curriculum, no DB seeding needed.
- **D-03:** Streak = derived at read time from progress_events (count of consecutive days with ≥1 event ending today or yesterday). No stored streak state to drift or forge.

### Server-verified completion (PROG-02)
- **D-04:** Lesson completion: `POST /api/progress/lesson` — accepts lessonId, but VERIFIES server-side that (a) the lesson exists in content, and (b) all of the lesson's challenges (if any) have a passing submission by this user recorded in DB. If the lesson has no challenges, viewing-completion is recorded on a legit authenticated POST (rate-limited later in Phase 6). The client cannot assert completion for lessons with challenges — the DB verdict is the proof.
- **D-05:** Challenge completion: automatic — when the runner worker writes a `passed` verdict onto a submission with a userId, it upserts a progress_event (contentId = challengeId). Zero new client surface; forging is impossible because the event derives from the sandbox verdict, not the request.
- **D-06:** All progress endpoints require an authenticated session (requireUser() guard); anonymous runs never record progress (ties to CHAL-03).

### Achievements (PROG-04)
- **D-07:** Award evaluation runs server-side after every progress_event insert: a pure function consumes (user's progress_events, passing submissions) and returns newly-earned achievement slugs; inserts are idempotent via the unique constraint. Initial defs (content-as-data): first-lesson, five-lessons, first-challenge, first-streak-3, html-foundations-complete. Award logic NEVER trusts client claims (DATA-MODEL principle 4).
- **D-08:** Achievement evaluation is best-effort: an award failure must not fail the progress write (wrapped, logged); a later event re-triggers evaluation, so nothing is permanently lost.

### Dashboard (PROG-01, PROG-03)
- **D-09:** `/dashboard` (authenticated, no-index): overall progress (% of curriculum lessons+challenges completed), per-track progress bars, current streak with today/yesterday markers, achievements grid (earned + locked), and "continue where you left off" (latest progress event → deep link). Reads are projections over progress_events + passing submissions — no new write paths.
- **D-10:** Header gains a Dashboard link for authenticated users (client-side session exists already in SiteHeader).

### UI (WEB-ONLY / PLAT-06)
- **D-11:** Dashboard is responsive: desktop = multi-column grid; mobile = stacked cards (no shrunken desktop). Progress bars are semantic (role=progressbar with aria values); the page is server-rendered from the session.

</decisions>

<specifics>
## Specific Ideas

- Continue-learning deep link derives from the last progress event's lesson position (linear order) — clicking resumes the curriculum.
- Streak computation utility is a pure function with unit tests (timezone-pinned) — streak bugs are notoriously easy to ship.
- Achievement award tests: forged client POSTs (no session, fake content ids) must be rejected or ignored — explicit negative tests for PROG-02.
- Idempotency tests: completing the same lesson twice yields one event; re-running a passed challenge yields one event.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Data + architecture
- `docs/DATA-MODEL.md` — ProgressEvent entity, design principles 1 & 4
- `src/lib/db/schema.ts` — existing tables (users, submissions with verdict data)
- `.planning/phases/02-data-auth-content-pipeline/02-CONTEXT.md` — D-09 (progress_events representation locked)

### Constraints + requirements
- `.planning/REQUIREMENTS.md` — PROG-01…04, PLAT-06, PLAT-07
- `.planning/ROADMAP.md` — Phase 4 success criteria
- `AGENTS.md` — web-only product constraint

### Prior-phase decisions
- `.planning/phases/03-challenge-loop-sandbox-execution/03-CONTEXT.md` — D-07 (immutable submissions, anonymous runs), verdict flow the challenge-completion hook rides on
- `src/lib/auth/guards.ts` — requireUser() reuse

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/lib/db/schema.ts` + migration flow — add progress_events + achievements here
- `src/workers/execute.ts` — the verdict write path where challenge completion hooks in
- `src/lib/auth/guards.ts` — requireUser() for the progress endpoints
- `src/lib/curriculum/loaders.ts` — lesson/challenge existence checks + linear order for "continue learning"
- `src/app/(auth)/layout.tsx` noIndexMetadata pattern + `src/lib/seo.ts` for the dashboard's no-index metadata
- SiteHeader (auth-aware) — add Dashboard link

### Established Patterns
- Zod validation at every boundary; server-only modules; DB-gated integration tests that skip cleanly
- Content-as-data with zod validation (achievements.json joins curriculum content)
- React-compiler-clean client components (no setState-in-render, refs written in effects only)

### Integration Points
- `completeJob()` in queue.ts writes the verdict → after it, insert progress_event + evaluate achievements
- SiteHeader → /dashboard link
- Sitemap: dashboard is NO-index → must NOT appear in sitemap.ts

</code_context>

<deferred>
## Deferred Ideas

- Rate limiting on the lesson-completion endpoint — Phase 6 hardening
- Achievement toasts/animations beyond accessible basics — Phase 6 a11y pass
- Cross-timezone streak edge-case UX copy — revisit with real user data
- Leaderboards / social progress sharing — Phase 5 community
- Server-side lesson "viewing completion" heuristics (scroll depth etc.) — not required, rejected as gameable

</deferred>

---

*Phase: 04-progress-achievements*
*Context gathered: 2026-09-02*
