# 2026-09-13 — "TypeError: Failed to fetch" in the console / challenge runs

**Symptom (learner report):** browser console shows `TypeError: Failed to fetch`
(challenge run requests dying); dev-server log showed server-side throws on
every curriculum consumer.

## Root cause (single, then cascading)

A **concurrently scaffolded course shell broke the global curriculum load.**
The C++ Intermediate authoring agent registered `cpp-intermediate` in
`cpp/track.json` while its `course.json` still had `"modules": []`.

1. `courseSchema` requires `.min(1)` modules → `loadCourse` throws (correct
   for finished content).
2. `loadTrack` eagerly loads **every** referenced course → the throw propagates
   to the global `getCurriculum` cache.
3. Every consumer of the global curriculum throws server-side: pages
   (`/learn/*` 500s), the sitemap, and the challenge **run API** (which
   resolves the challenge server-side). Requests that die mid-flight surface
   in the browser as `TypeError: Failed to fetch`.

Later in the session the same class reappeared twice, progressively deeper:
- `TrackPage` / course-page & practice-page `generateStaticParams` iterated
  `track.courses` **raw manifest references** and called `getCourse` per ref
  → `CurriculumNotFoundError` for the (correctly) skipped shell.
- The other agent's newest MDX lessons contained raw C++ generics
  (`<typename T, ...>`, `operator<`) outside code contexts → MDX parsed them
  as JSX tags → Turbopack build error → **every** page (the static mdx-map
  imports all lessons) rendered the Next "Build Error" overlay.

## Fixes

- **`loaders.ts`** — `isAuthoringShell()`: a *parseable* course.json with an
  explicit empty `modules` array is a deliberate authoring scaffold; `loadTrack`
  excludes it instead of failing the whole curriculum. Missing/unparseable
  files and any other invalid content still throw loudly. Added
  `getLoadedCourses(trackId)` returning only loaded courses in manifest order.
- **Track page** — builds course cards from `getLoadedCourses` instead of raw
  `track.courses` references. **Course page + both practice pages'
  `generateStaticParams`** — same: pre-render only loaded courses (a shell has
  no page to render).
- **Unit test** — `curriculum-loaders.test.ts` now asserts `toContain`
  ("cpp-beginner") instead of pinning the exact course list, since the track
  manifest legitimately lists a concurrently scaffolded course.
- **Three MDX lines in the other agent's in-progress templates lessons**
  (minimal, content-preserving syntax repairs): joined a code span that a
  line break split (leaving `<typename T, …>` bare to JSX), and wrapped two
  `"… operator<"` contract sentences in backticks so `<` isn't a pseudo-tag.
  Same bug class I fixed in my own C++ Beginner course earlier today.

## Verification (measured, not assumed)

- Full unit suite **160/160** (27 files) with the shell still on disk — was
  22 failures before the loader fix. Typecheck ✅, lint ✅.
- Curriculum validator: all 3 tracks load, EN/VI synced, linear paths
  web 143 / python 169 / cpp 65.
- **Critical-path E2E 2/2** (`register → browse → run challenge → verdict →
  dashboard` + keyboard-only run) — the exact loop that produced
  "Failed to fetch" now passes in a real browser against real infra
  (dev server on :3456, worker, Postgres, sandbox).
- Live routes on the restored preview (:3000): `/`, `/learn`, `/learn/cpp`,
  `/learn/cpp/cpp-beginner`, `/learn/python/python-advanced` all 200.

## Environment notes (for future sessions)

- Next 16 allows **one dev server per project directory**: the user's :3000
  preview and the E2E webServer (:3456) cannot run simultaneously. To run
  E2E: stop :3000, `rm -f .next/dev/lock` (stale lock outlives a kill -9),
  run E2E detached (`nohup … &` survives tool timeouts; foreground runs get
  reaped and orphan the worker), then restore :3000. `reuseExistingServer`
  attaches to a healthy existing :3456 if one is already up.
- The challenge **runner worker** (`pnpm worker`) must be running or every
  challenge run hangs. After killing processes during E2E setup, restore it.
- The concurrent C++ Intermediate agent is actively landing content (shell
  now still `modules: 0`, MDX lessons flowing in). Their next MDX batch may
  reintroduce the JSX-trap bug class — the fence-aware scanner pattern from
  this session (`strip fences → strip inline code → flag bare `<` followed by
  identifier-ish content`) is the tool to run when pages 500 again.
