# Phase 11 — Course 2: Web Development Intermediate — SUMMARY

Date: 2026-09-12 (content authored 2026-09-05 → 2026-09-12; gates re-verified post-restart)
Status: **COMPLETE**

## Research
`docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-INTERMEDIATE.md` — MDN, web.dev, OWASP Top-10, Node.js / TypeScript / PostgreSQL docs, The Odin Project, freeCodeCamp, Full Stack Open, developer-roadmap sources. Used to shape an original Code Journey curriculum; no curriculum text copied. Key findings applied: deliberate-practice evidence (practice-first density), diagnose-don't-memorize pedagogy for performance/security, "engineering mindset" progression (following instructions → solving problems → engineering applications).

## Curriculum (measured on disk)
- **13 modules**: Modern JS → Advanced DOM → Async/APIs → Advanced CSS/UI → TypeScript → Git Workflow → Testing & Debugging → Performance → Security → Backend (Node) → Databases/Full-Stack → Production → Capstone
- **80 lessons** (EN `.mdx` + VI `.vi.mdx` sidecars), **63 practice sets**, **181 challenges** (169 practice + 12 lesson-attached checkpoint incl. capstone verification)
- Prerequisite `web-development-beginner` enforced in course.json + prerequisite UI (EN/VI)
- Declared time ~2,571 min (~43 h); practice-first loop: learn → micro-practice → guided → independent → debug → mini-build → project

## Projects
Data Explorer · Interactive Dashboard · API-Powered App · SaaS Dashboard · Type-Safe API Client · Repo Simulation · Test & Repair · Performance Optimization · Security Audit · REST API · Full-Stack CRUD · Ship It · **Capstone: ServiceDesk** (requirements-only; graded via decision-verification challenges).

## English / Vietnamese
Full parity — VI `.vi.mdx` sidecars + `.vi.json` practice overlays (same overlay mechanism as Beginner); grading code shared across locales; `validate-content.ts` verifies EN/VI structural sync for both courses and loads every node through schema-validating loaders in **both locales**.

## Verification (re-run from scratch 2026-09-12)
| Gate | Result |
| --- | --- |
| validate-content.ts | PASS — both courses × both locales (259 + 401 nodes each) |
| Challenge harness (intermediate) | **181/181** (ref passes + wrong fails) |
| Beginner harness (regression) | **91/91** |
| Unit/integration | **160/160** (27 files) |
| E2E | **36/36** (mobile 375px, keyboard-only, a11y, SEO static render) |
| Typecheck / lint | PASS / 0 errors 0 warnings |
| Production build | PASS — 538 static pages |

## Issues found & fixed (real)
- VI course page 404: `course.vi.json` `audience` exceeded the 400-char zod limit → loader threw on every VI request. Fixed (389 chars) + both-locale loader sweep added to `validate-content.ts`, fault-injection proven.
- course.json module refs vs disk IDs mismatch — aligned.
- Cross-course ID collisions (`workflow-checkpoint`, `components-practice`) — renamed.
- 7 checkpoints with invalid `level: "checkpoint"` — moved to valid levels.
- Practice sets declared but never authored (Module 2 ×3, Module 12 ×3, capstone) — authored + harness-verified.
- Harness solutions must be self-contained (boilerplate not prepended) — fixed where violated.
- Recurring authoring-script escaping defects (nested quotes in Python/JS literals) — root-caused; pipeline switched to Python triple-quoted MDX + `json.dump`.

## Leftovers (not regressions)
- ~396 files uncommitted on `main` (user decision).
- Repo-wide prettier drift (~304 pre-existing files, incl. untouched Beginner content) — separate decision.

## Final Status
**COURSE 2 — WEB DEVELOPMENT INTERMEDIATE: COMPLETE** — all gates green, Beginner intact, both locales synchronized and loader-verified.
