# Requirements: Code Journey

**Defined:** 2026-09-02
**Core Value:** A student can learn to code for free through structured lessons, practice in auto-graded interactive challenges (sandboxed execution), and see real verified progress — with an AI mentor that teaches instead of solving.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Authentication

- [ ] **AUTH-01**: User can create an account with email and password
- [ ] **AUTH-02**: User can log in with email/password and stay logged in across sessions
- [ ] **AUTH-03**: User can log in with GitHub OAuth
- [ ] **AUTH-04**: User can log out from any page
- [ ] **AUTH-05**: User can reset their password via an emailed link

### Curriculum

- [ ] **CURR-01**: Visitor can browse tracks, courses, and lessons without an account
- [ ] **CURR-02**: User can view a lesson rendered from structured content (explanations + code examples)
- [ ] **CURR-03**: User can navigate a track in linear order (previous/next lesson)
- [ ] **CURR-04**: All curriculum content validates against a zod schema at build time (content-as-data; invalid content fails the build)

### Challenges

- [ ] **CHAL-01**: User can write code in a browser-based editor on a challenge page
- [ ] **CHAL-02**: User can run their code against the challenge's tests and see pass/fail per test
- [ ] **CHAL-03**: User can submit a passing solution and have it recorded server-side
- [ ] **CHAL-04**: User-submitted code executes only inside an isolated sandbox (no network access, memory/CPU limits, execution timeouts, non-root, ephemeral filesystem)
- [ ] **CHAL-05**: User sees educational test-failure output (which test failed and why, not just a boolean)
- [ ] **CHAL-06**: User's in-progress code persists across page refreshes (draft storage)

### Progress

- [ ] **PROG-01**: User can see completion state for lessons and challenges they have finished
- [ ] **PROG-02**: Progress is recorded only via server-verified events (client cannot mark itself complete)
- [ ] **PROG-03**: User can see their streak of consecutive active days
- [ ] **PROG-04**: User can earn achievements for defined milestones

### Community

- [ ] **COMM-01**: User can post a question or comment on a lesson
- [ ] **COMM-02**: User can reply to an existing comment
- [ ] **COMM-03**: Visitor can read discussion threads without an account

### AI Mentor

- [ ] **AI-01**: User can request a graduated hint on a challenge; the mentor never returns a complete solution
- [ ] **AI-02**: User can ask the mentor to explain an error message from their failed run
- [ ] **AI-03**: Mentor usage is rate-limited per user
- [ ] **AI-04**: The platform is fully functional when no AI provider key is configured (mentor features degrade gracefully)

### Platform Foundation

- [ ] **PLAT-06**: Every user-facing feature is usable as responsive web UI — desktop, laptop, tablet, and an intentionally designed mobile layout (not a shrunken desktop); panels may reflow into tabs/drawers/stacked sections
- [ ] **PLAT-07**: Public educational pages are indexable (SEO) and private user data is never exposed to search engines (no-index on authed pages)
- [ ] **PLAT-08**: All student-code execution and AI calls go through server-side web APIs; the browser never executes student code with platform privileges
- [ ] **PLAT-01**: A developer can clone the repo, install dependencies, and start the full dev environment using only documented commands
- [ ] **PLAT-02**: `pnpm typecheck`, `pnpm lint`, and `pnpm test` pass and are wired as required checks
- [ ] **PLAT-03**: All interactive UI is keyboard-navigable and meets WCAG 2.1 AA contrast requirements
- [ ] **PLAT-04**: No secrets are committed; `.env.example` documents every required environment variable
- [ ] **PLAT-05**: Core behavior is covered by automated tests (unit tests for libraries, E2E for the critical path)

## v2 Requirements

### Platform Expansion

- **NATIVE-01 (BARRED)**: Native desktop/mobile apps — permanently excluded by the web-only product constraint unless requirements explicitly change

### Delivery Expansion

Deferred to future release. Tracked but not in current roadmap.

### Execution Expansion

- **EXEC-01**: Python track with sandboxed execution
- **EXEC-02**: SQL challenges with sandboxed database instances
- **EXEC-03**: Compiled-language support (Java, C, C++, Go, Rust) via per-language images

### Product Expansion

- **CERT-01**: Certificates of completion for finished tracks
- **PROJ-01**: Portfolio projects with submission gallery
- **IDE-01**: Full in-browser development environment (virtual filesystem, terminal)
- **CLASS-01**: Classroom/team mode for educators
- **NOTIF-01**: Email notifications for replies and achievements
- **CONTRIB-01**: Community curriculum contributions via reviewed PR workflow

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Paid tiers / paywalled content | Violates the core mission: free education for everyone |
| AI auto-solve button | Anti-feature — destroys learning outcomes; hints only |
| Real-time collaborative coding rooms | High complexity, low v1 value |
| User-created courses (UGC) | Moderation burden and trust risk; curated content only |
| Global leaderboards | Toxic competition and cheating incentive at launch |
| Native desktop apps (Tauri/Electron) | Web-only product constraint (2026-09-02): the website is the product; no shell wrapper |
| Native mobile apps (React Native/Flutter) | Web-only product constraint (2026-09-02): responsive web first; no native targets |
| Kubernetes production deployment | Premature at current scale; Docker Compose until load demands more |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLAT-01 | Phase 1 | Pending |
| PLAT-02 | Phase 1 | Pending |
| PLAT-04 | Phase 1 | Pending |
| PLAT-07 | Phase 2 | Pending |
| AUTH-01 | Phase 2 | Pending |
| AUTH-02 | Phase 2 | Pending |
| AUTH-03 | Phase 2 | Pending |
| AUTH-04 | Phase 2 | Pending |
| AUTH-05 | Phase 2 | Pending |
| CURR-01 | Phase 2 | Pending |
| CURR-02 | Phase 2 | Pending |
| CURR-03 | Phase 2 | Pending |
| CURR-04 | Phase 2 | Pending |
| CHAL-01 | Phase 3 | Pending |
| PLAT-08 | Phase 3 | Pending |
| CHAL-02 | Phase 3 | Pending |
| CHAL-03 | Phase 3 | Pending |
| CHAL-04 | Phase 3 | Pending |
| CHAL-05 | Phase 3 | Pending |
| CHAL-06 | Phase 3 | Pending |
| PROG-01 | Phase 4 | Pending |
| PROG-02 | Phase 4 | Pending |
| PROG-03 | Phase 4 | Pending |
| PROG-04 | Phase 4 | Pending |
| COMM-01 | Phase 5 | Pending |
| COMM-02 | Phase 5 | Pending |
| COMM-03 | Phase 5 | Pending |
| AI-01 | Phase 5 | Pending |
| AI-02 | Phase 5 | Pending |
| AI-03 | Phase 5 | Pending |
| AI-04 | Phase 5 | Pending |
| PLAT-03 | Phase 6 | Pending |
| PLAT-05 | Phase 6 | Pending |
| PLAT-06 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 34 total
- Mapped to phases: 34
- Unmapped: 0 ✓

---
*Requirements defined: 2026-09-02*
*Last updated: 2026-09-02 — web-only product correction applied (PLAT-06/07/08 added)*
