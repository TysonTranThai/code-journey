# Phase 2: Data, Auth & Content Pipeline - Context

**Gathered:** 2026-09-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 delivers the identity and data layer plus the curriculum content pipeline: a working PostgreSQL database via Docker Compose, Auth.js-based authentication (email/password + GitHub OAuth + password reset), a zod-validated content-as-data curriculum, and the public browsing UI (tracks → courses → lessons) that is responsive and SEO-conscious. The code execution sandbox, challenge grading, progress recording, discussions, and AI mentor are later phases and are out of scope. Standing product constraint: WEB-ONLY — responsive web UI, server-side services behind APIs, SEO for public content, no-index for private pages.

</domain>

<decisions>
## Implementation Decisions

### Authentication stack (resolves the previously-documented UNKNOWN)
- **D-01:** Use **next-auth@5.0.0-beta.32** (Auth.js v5), pinned exact — NOT the stable v4.24.15 tag. Verified 2026-09-02 from the npm registry: v5-beta.32 peer-depends on `next ^14 || ^15 || ^16` and `react ^19` explicitly, and is the actively maintained Auth.js line for App Router; v4 is the legacy line (pre-RSC internals, old jose 4 / openid-client 5 dependency set). Fallback if blocked at execution: v4.24.15 (documented, not expected).
- **D-02:** Adapter: **@auth/drizzle-adapter@1.11.3** — verified it depends on `@auth/core@0.41.3`, the exact core version next-auth@5.0.0-beta.32 bundles. No version drift.
- **D-03:** Email/password via the Credentials provider; password hashing with **bcryptjs@3.0.3** (pure JS — no native-build risk), cost factor 12. argon2 (0.45.1) rejected for Phase 2: native module adds install fragility; revisit later if desired.
- **D-04:** Session strategy = **"jwt"** (required by Auth.js when a Credentials provider is used — database sessions and Credentials are incompatible). Sessions are JWE cookies (httpOnly, secure in prod, sameSite lax), verified server-side via `auth()` in RSCs/server actions. The adapter's standard tables (users, accounts, sessions, verification_tokens) are still created; `sessions`/`verification_tokens` remain for OAuth/email-provider paths.
- **D-05:** GitHub OAuth is env-gated: the provider is registered only when `GITHUB_CLIENT_ID`/`GITHUB_CLIENT_SECRET` are set. Dev credentials stay placeholders; no real OAuth app is created in this phase. Nodemailer is NOT installed (its peer dep is optional, verified) — the "dev email transport" logs reset links to the server console.
- **D-06:** Password reset (AUTH-05): `password_reset_tokens` table (sha256-hashed random 32-byte token, 1-hour expiry, single-use, `usedAt`), request endpoint always responds generically (no user enumeration), reset page consumes the token. No email verification in v1 (no requirement asks for it).

### Database
- **D-07:** PostgreSQL via Docker Compose, image **postgres:16-alpine** (tag verified on Docker Hub 2026-09-02), host port **5433** (5432 commonly taken on this machine), db/user/password `codejourney`, named volume for data. Postgres 17/18 images exist but the project pins 16 per STACK.md research.
- **D-08:** ORM: **drizzle-orm@0.45.2** + **drizzle-kit@0.31.10** (verified latest tags, matches STACK.md pairing), driver **postgres@3.4.9** (postgres-js). Schema in `src/lib/db/schema.ts`, migrations in `src/lib/db/migrations/` (generated SQL committed to git). `drizzle.config.ts` reads `DATABASE_URL` from env.
- **D-09:** DB stores **user-generated state only** (per docs/DATA-MODEL.md principle 2): auth tables + profiles. Curriculum is content-as-data, NOT database rows — a deliberate, documented deviation from "curriculum core" phrasing in the roadmap plan title. Scripts: `db:up`/`db:down`/`db:reset`/`db:generate`/`db:migrate`/`db:seed`/`db:studio` (runner: tsx@4.23.13, verified current).
- **D-10:** `pnpm db:seed` seeds **identity fixtures only** (dev student + dev admin with bcrypt-hashed passwords, idempotent upserts). Curriculum content ships as version-controlled files under `src/content/`, not seeds.
- **D-11:** Progress representation is DECIDED now, implemented in Phase 4: an append-only `progress_events` table keyed (userId, contentType ∈ {lesson, challenge}, contentId) with a uniqueness constraint, written only by server-verified paths. No table, endpoint, or UI in Phase 2 (Phase 2 success criteria don't include progress recording; avoids dead code).

### Authorization
- **D-12:** Three access levels, no more: **anonymous visitor** (public curriculum), **student** (any authenticated user, default role), **admin** (`users.role` enum `student | admin`, default `student`). Server-side guards `requireUser()` and `requireRole('admin')` live in `src/lib/auth/guards.ts`; authorization is never decided in the client. No admin UI exists in Phase 2 — admin capability is a stored role + guard, so nothing is exposed "just because a URL exists".

### Content-as-data architecture
- **D-13:** Curriculum = **JSON metadata files + MDX bodies** under `src/content/tracks/<trackId>/` (JSON per track/course/module/lesson for structure + metadata; lesson bodies as `.mdx` referenced by relative path). JSON (not YAML frontmatter) is chosen because frontmatter inside `.mdx` would require remark-frontmatter tooling with @next/mdx, and JSON gives a single, perfectly zod-validatable structure. Zod 4 schemas in `src/lib/curriculum/schema.ts` validate: id format, unique ids across the curriculum, unique slugs, ordering, required lesson fields, difficulty, minutes > 0, and that every `contentPath` resolves to an existing file (cross-references validated).
- **D-14:** MDX rendering via **@next/mdx@16.3.4** (matches Next 16.3.4 exactly) + **@mdx-js/mdx 3.1.1** + **remark-gfm@4.0.1** + **rehype-slug@6.0.0** (all versions verified). Lesson pages use a static import map (`src/lib/curriculum/mdx-map.ts`) so Turbopack compiles content MDX at build. All versions verified current. Fallback if the import-map approach misbehaves under Turbopack: compile bodies programmatically with `@mdx-js/mdx` `compile()` at load — decide at execution, both are in-repo patterns.
- **D-15:** Validation runs at module load of the loader barrel (statically imported by pages), so **invalid content fails `pnpm build`** with a named zod error path — satisfying CURR-04's "fails the build". Unit tests assert the failure mode with invalid fixtures (missing field, duplicate id, broken contentPath, empty module).

### Curriculum UX + SEO (WEB-ONLY constraint applied)
- **D-16:** Routes: `/learn` (tracks), `/learn/[trackId]` (courses), `/learn/[trackId]/[courseId]` (modules overview), `/learn/[trackId]/[courseId]/[lessonId]` (lesson). All public pages statically rendered (`generateStaticParams`) — fast and crawlable.
- **D-17:** SEO (PLAT-07): `generateMetadata` with title template + descriptions + canonical `alternates` on public pages; `src/app/sitemap.ts` generated from curriculum loaders; `src/app/robots.ts` allows public content and disallows `/api`; login/register/reset pages set `robots: { index: false }`. Claimed only after implemented: metadata, sitemap, robots, semantic HTML. JSON-LD structured data is deferred (documented, not implemented silently).
- **D-18:** Responsive (PLAT-06 foundation): mobile-first Tailwind; course grids 1 → 2 (sm) → 3 (lg) columns; lesson body max-w-prose; header collapses to a disclosure menu (aria-expanded) on mobile. Intentionally designed, not a shrunken desktop. WCAG 2.1 AA full pass remains Phase 6; semantic HTML + keyboard-operable nav are standards from day one (docs/ACCESSIBILITY.md).
- **D-19:** Product identity: dark developer-first aesthetic established in Phase 1 (zinc-950 / indigo accent) extends to curriculum pages; clean, modern, friendly — no admin-dashboard feel. No large visual redesign in this phase.

### the agent's Discretion
- Exact Tailwind class choices within the established dark/indigo identity
- Prose styling approach for lesson MDX (scoped utility classes; avoid adding typography plugins unless verified)
- Dev fixture password values (documented in seed script, obviously fake)
- Exact MDX component styling/mapping (h2/h3/code/pre renderers)

</decisions>

<specifics>
## Specific Ideas

- The seed curriculum follows the user's worked example: course **Web Development Foundations**, module **HTML Foundations**, lessons: Introduction to HTML, Elements, Attributes, Links, Images — each 200–400 words of real educational MDX with code examples. Challenge entries exist in the module JSON as an empty `challenges: []` array so Phase 3 plugs in without schema churn; challenge CONTENT itself is Phase 3 (no runner exists to give it meaning).
- "Where am I, what's next": every lesson page shows breadcrumb (track → course → module), estimated minutes, and prev/next pager that crosses module boundaries in linear track order.
- Landing page CTA switches from the health-check link to `/learn` in this phase.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Data + architecture
- `docs/DATA-MODEL.md` — Entity model and Phase 2 rows (User, Profile, Session; curriculum is content-as-data); progress-as-event-log decision
- `docs/ARCHITECTURE.md` — Module seams (lib/db, lib/auth, lib/curriculum), content-as-data pattern, monolith boundaries
- `.planning/research/STACK.md` — Pinned versions and pairing rules (drizzle-orm ↔ drizzle-kit)
- `.planning/research/ARCHITECTURE.md` — Content-as-data rationale, anti-patterns (hardcoded curriculum, client-trusted progress)

### Security
- `docs/SECURITY.md` — Auth posture planned for Phase 2 (sessions, hashing, validation, XSS/CSRF baseline); what must NOT be claimed as verified
- `docs/ACCESSIBILITY.md` — Semantic HTML, focus states, keyboard navigation standards

### Requirements + constraints
- `.planning/REQUIREMENTS.md` — AUTH-01…05, CURR-01…04, PLAT-06/07/08 definitions
- `.planning/ROADMAP.md` — Phase 2 success criteria and plan list; standing WEB-ONLY constraint block
- `AGENTS.md` — Product type constraint (web-only) and tech stack table

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/lib/site-config.ts` — site name/tagline/description; reuse for metadata templates
- `src/app/layout.tsx` — root layout with metadata template + skip link; header/nav integrates here
- `src/app/page.tsx` — landing page (dark zinc/indigo identity); CTA swap task lands here
- `src/app/health/route.ts` + `tests/unit/health.test.ts` — the testing conventions to follow (vitest 4, `@/` alias, node environment)

### Established Patterns
- Tailwind 4 utility classes, no config file (CSS-first)
- ESLint flat config (`eslint-config-next/core-web-vitals` + `/typescript` subpaths) — keep new files compliant
- TypeScript strict + `noUncheckedIndexedAccess` — schema/loader code must respect it
- Prettier formatting gate (`pnpm format:check`) — run before commit

### Integration Points
- `.env.example` already declares `DATABASE_URL` (port 5433), `AUTH_SECRET`, `AUTH_URL`, `GITHUB_CLIENT_ID/SECRET`, `EMAIL_FROM`, `SMTP_URL` — Phase 2 consumes exactly these; SMTP_URL stays optional (dev transport = console)
- `tsconfig.json` paths `@/*` → `./src/*`; `resolveJsonModule` already on (JSON content imports work)
- `vitest.config.ts` includes `tests/**/*.test.ts` — new test dirs must match this glob (e.g. `tests/unit/…`, `tests/integration/…`)

</code_context>

<deferred>
## Deferred Ideas

- Progress recording (table + endpoints + UI) — Phase 4 (representation decided in D-11)
- Challenge content, test cases, and the sandbox loop — Phase 3
- Discussions and AI mentor — Phase 5
- Full WCAG 2.1 AA audit + E2E (Playwright) suite — Phase 6
- JSON-LD structured data for lessons — nice-to-have; document when done, never claim silently
- Email verification of new accounts — no v1 requirement; revisit with real email transport

</deferred>

---

*Phase: 02-data-auth-content-pipeline*
*Context gathered: 2026-09-02*
