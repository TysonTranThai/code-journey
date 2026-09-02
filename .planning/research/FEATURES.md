# Feature Research

**Domain:** Coding education platform (online judge + LMS + community)
**Researched:** 2026-09-02
**Confidence:** MEDIUM-HIGH (based on established competitors: freeCodeCamp, Exercism, Codecademy, LeetCode, The Odin Project, Scrimba)

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Account + auth (email/password, OAuth) | Identity precedes progress | MEDIUM | Auth.js line; email verification + reset expected |
| Structured curriculum with tracks/courses/lessons | The core LMS promise | MEDIUM | Content-as-data (MDX or DB) |
| Interactive coding challenges with auto-graded tests | The freeCodeCamp core loop | HIGH | Needs sandbox execution + per-challenge test harness |
| Progress tracking (lesson/challenge completion, streaks) | Retention mechanic #1 | MEDIUM | Progress model must be event-sourced-ish from day 1 |
| Browser code editor | Friction-free practice | MEDIUM | Monaco (VS Code editor) is the standard embed |
| Certificates of completion | Motivation + shareability | LOW | Later, but schema should anticipate |
| Responsive web (mobile-consumable lessons) | Most first visits are mobile | MEDIUM | Challenges stay desktop-first initially |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| AI mentor that teaches, never solves | Pedagogy-first AI is rare and on-mission | MEDIUM-HIGH | Guardrails: hints, Socratic questioning, error explanation; never full solutions |
| Modern, fast, accessible UI (WCAG 2.1 AA) | freeCodeCamp's UI is dated; a11y is a real differentiator | MEDIUM | Accessibility from foundation phase |
| Multi-language support beyond JS (Python, SQL, Go, Rust …) | Most free platforms are JS-centric | HIGH | Only after JS track proves the pipeline |
| Project-based portfolio tracks | Employers value projects over badges | MEDIUM | GitHub-integrated submissions later |
| Community discussions anchored to lessons | Social learning loop | MEDIUM | Threads per lesson/challenge |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| AI auto-solve button | Convenience | Kills learning; on-mission anti-feature | AI gives graduated hints only |
| Real-time collaborative coding rooms | "Like Replit!" | High complexity, low initial value | Async code review later |
| Custom user-hosted content / courses | "UGC!" | Moderation burden + trust risk | Curated content; contributions via PRs |
| Gamification explosion (leaderboards everywhere) | Engagement | Toxic competition, cheating incentive | Personal streaks + achievements first |

## Feature Dependencies

```
[Sandbox execution service]
    └──requires──> [Container runtime / isolation strategy]
                       └──requires──> [Resource limits + timeouts policy]

[Auto-graded challenges] ──requires──> [Sandbox execution service]
[Auto-graded challenges] ──requires──> [Submission model + test harness format]
[Progress tracking] ──requires──> [Auth + curriculum model]
[AI mentor] ──enhances──> [Challenges + lessons]  (requires AI provider key + guardrail design)
[Certificates] ──requires──> [Progress tracking]
[Discussions] ──requires──> [Auth]
```

### Dependency Notes

- **Challenges require sandbox:** no auto-grading without safe execution; this is the critical path of the whole product
- **AI mentor enhances but never gates:** platform must be fully usable with AI disabled
- **Progress requires auth:** anonymous progress = local-storage only, explicitly deferred

## MVP Definition

### Launch With (v1)

- [ ] Auth (email/password + GitHub OAuth) — identity foundation
- [ ] Curriculum browser (tracks → courses → lessons, content-as-data)
- [ ] Interactive JS/TS challenges in browser editor (Monaco) with sandbox auto-grading
- [ ] Progress tracking + basic achievements/streaks
- [ ] AI mentor (hint/explain modes with anti-solve guardrails) — optional, flagged
- [ ] Accessible, responsive foundation UI

### Add After Validation (v1.x)

- [ ] Discussions/comments on lessons and challenges
- [ ] Projects with submission gallery
- [ ] Certificates
- [ ] Python + SQL tracks (extends sandbox)

### Future Consideration (v2+)

- [ ] Multi-language expansion (Java, C, C++, Go, Rust)
- [ ] Full in-browser dev environment (virtual filesystem, terminal)
- [ ] Mobile apps, offline mode
- [ ] Team/classroom mode for educators

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Curriculum browser | HIGH | MEDIUM | P1 |
| Auth + profiles | HIGH | MEDIUM | P1 |
| JS/TS challenge loop w/ sandbox grading | HIGH | HIGH | P1 |
| Progress + streaks | HIGH | LOW-MEDIUM | P1 |
| AI mentor (guarded) | HIGH | MEDIUM | P2 |
| Monaco-based editor UX | HIGH | MEDIUM | P2 |
| Discussions | MEDIUM | MEDIUM | P2 |
| Multi-language sandbox | MEDIUM | HIGH | P3 |
| Certificates | MEDIUM | LOW | P3 |
| Full browser IDE | MEDIUM | VERY HIGH | P3 |

## Competitor Feature Analysis

| Feature | freeCodeCamp | Exercism | Codecademy | Our Approach |
|---------|--------------|----------|------------|--------------|
| Curriculum structure | Certifications, linear | Tracks, mentoring | Career paths | Tracks/courses/lessons, content-as-data |
| Code execution | In-browser JS + iframe tests | Local CLI + web editor | Cloud IDE | Sandboxed container execution + Monaco |
| AI help | Limited | AI hints available | AI assistant | Pedagogy-first AI mentor, provider-agnostic |
| Community | Forum + campers | Mentoring + community | Paid forums | Threaded discussions anchored to content |
| Cost | Free | Free (OSS) | Freemium | Free, mission-bound |

## Sources

- freeCodeCamp (github.com/freecodecamp), Exercism, Codecademy, LeetCode product surfaces — MEDIUM-HIGH
- Prior art on grading pipelines: Judge0 docs, Exercism architecture talks — MEDIUM

---
*Feature research for: Code Journey — free coding education platform*
*Researched: 2026-09-02*
