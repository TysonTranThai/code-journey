# Data Model (Conceptual)

**Status:** DESIGN ONLY — no schema is implemented yet (Drizzle schema lands in
Phase 2; execution/progress tables in Phases 3–4). This document fixes the model and
relationships so the implementation stays coherent.

## Entity Overview

```
User 1──1 Profile
User 1──* Session                      (auth)
User 1──* ProgressEvent  *──1  (Lesson | Challenge)
User 1──* Submission     *──1 Challenge
Challenge *──1 Lesson
Challenge 1──* TestCase
Lesson *──1 Module  *──1 Course  *──1 Track
User 1──* Achievement *──1 AchievementDef
User 1──* DiscussionThread 1──* Comment *──1 User (author)
User 1──* MentorSession 1──* MentorMessage
ExecutionJob 1──1 Submission
```

## Entities and Purpose

| Entity           | Purpose                                                 | Key relationships                                  | Phase               |
| ---------------- | ------------------------------------------------------- | -------------------------------------------------- | ------------------- |
| User             | Account identity (email/password + OAuth identities)    | has profile, sessions, progress                    | 2                   |
| Profile          | Display name, avatar, bio                               | belongs to user                                    | 2                   |
| Session          | Auth session (server-validated)                         | belongs to user                                    | 2                   |
| Track            | Top curriculum container (e.g. Foundations)             | has courses                                        | 2 (content-as-data) |
| Course           | Ordered module group                                    | belongs to track                                   | 2 (content-as-data) |
| Module           | Ordered lesson group                                    | belongs to course                                  | 2 (content-as-data) |
| Lesson           | Learning content unit                                   | belongs to module; may have challenges             | 2                   |
| Challenge        | Auto-graded exercise                                    | belongs to lesson; has test cases; has submissions | 3                   |
| TestCase         | One assertion with educational failure message          | belongs to challenge                               | 3                   |
| Submission       | One attempt: code snapshot + verdict + per-test results | belongs to user + challenge                        | 3                   |
| ExecutionJob     | Queue entry for the runner (status, claims, timing)     | 1:1 with submission                                | 3                   |
| ProgressEvent    | Append-only, server-verified completion event           | belongs to user + content ref                      | 4                   |
| AchievementDef   | Milestone definition (id, criteria, icon)               | has awards                                         | 4                   |
| Achievement      | A user earning a def (awarded server-side)              | belongs to user + def                              | 4                   |
| DiscussionThread | Question/discussion anchored to a lesson or challenge   | has comments                                       | 5                   |
| Comment          | Reply in a thread                                       | belongs to thread + author                         | 5                   |
| MentorSession    | One AI-mentoring conversation with guardrail state      | belongs to user; has messages                      | 5                   |
| MentorMessage    | Single mentor/user message (+ refusals logged)          | belongs to session                                 | 5                   |

## Design Principles

1. **Progress is an event log, not a flag.** Completions are rows in `ProgressEvent`
   written only by server-verified paths (graded submission, lesson-completion
   endpoint backed by server checks). The UI reads projections; the client never
   asserts completion.
2. **Curriculum content lives in git, not the database.** Tracks/courses/modules/
   lessons are content-as-data files validated with zod at build time. The database
   stores user-generated state only. (TestCases may live in content files too; the
   verdict rows are DB.)
3. **Submissions are immutable snapshots.** Code, verdict, per-test results, and
   execution metadata are written once by the runner; edits create new rows.
4. **Achievements are derived from events.** Award logic consumes ProgressEvent /
   Submission streams; it never trusts client claims.
5. **AI mentor conversations are first-class records.** Guardrail refusals are logged
   as messages so the anti-solve behavior is auditable and testable.

## v2+ (documented, deferred)

- Certificate (issued from verified progress; PDF/OG image)
- Project / ProjectSubmission (portfolio tracks)
- Notification (email/in-app)
- LanguageRuntime registry (per-language sandbox images for Phase v2 execution)
