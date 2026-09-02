---
phase: 03-challenge-loop-sandbox-execution
plan: 04
---

# Plan 03-04 Report: Challenge Workspace UI

**Completed:** 2026-09-02

## What Was Built

1. **Challenge route** — `/learn/[trackId]/[courseId]/[moduleId]/[lessonId]/challenge/[challengeId]` (03-CONTEXT D-09): under its lesson, breadcrumbs preserved, public + indexable (PLAT-07), canonical URL, 404 via notFound() for unknown ids.
2. **ChallengeWorkspace** (`src/components/challenge/ChallengeWorkspace.tsx`) — responsive workspace (PLAT-06):
   - Desktop (lg+): side-by-side instructions+Run | editor+output
   - Tablet/mobile: accessible tab switcher (`MobileTabs`, role=tablist/tab/tabpanel, arrow-free click tabs with focus outlines) — Instructions / Code / Output — an intentional mobile layout, not a shrunken desktop
   - Run button posts to `/api/challenges/run`, polls the verdict endpoint (1s, capped ~20s), renders per-test educational results (CHAL-05); distinct pending/timeout/error/failed states; disabled during run
3. **CodeEditor** — `@monaco-editor/react@4.7.0` + `monaco-editor@0.54.0` (versions verified live; React 19 peer-compatible), vs-dark theme, aria-label, HTML mode.
4. **VerdictPanel** — pass/fail per test with hint text, timeout copy ("check for infinite loops"), error output pane, aria-live polite, reduced-motion spinner.
5. **Draft persistence** (`src/lib/challenges/use-draft.ts`, CHAL-06) — localStorage keyed `cj-draft:<challengeId>`, SSR-safe hydration (rAF-deferred to avoid cascading renders), reset-to-starter link when a draft exists.
6. **Lesson page** — new "Practice" section listing the lesson's challenges with difficulty badges, linking to the challenge workspace.

## react-compiler Compliance

Three lint errors from the new compiler rules were fixed structurally (no disables):
- self-referencing poll callback → poll loop behind a ref assigned in an effect
- setState in effect (draft hydration) → rAF-deferred write with cleanup
- MDX component render (pre-existing) → createElement (committed in 03-01)

## Verification

- Gates: format ✓, lint ✓, typecheck 0 errors, **tests 59/59** (incl. Docker-gated isolation suite), `pnpm build` clean with challenge routes present
- **Live end-to-end loop** (server + worker + sandbox):
  - correct solution → `202` → verdict `passed`, 3/3 tests, 583ms
  - failing solution → `failed` with per-test educational hints rendered
  - unknown challenge → 404; invalid body → 400
  - anonymous submissions recorded with `user_id = null` (CHAL-03)
  - challenge page HTTP 200; lesson page shows Practice links

## Files

- `src/components/challenge/ChallengeWorkspace.tsx`, `CodeEditor.tsx`, `VerdictPanel.tsx`, `MobileTabs.tsx` (new)
- `src/lib/challenges/use-draft.ts` (new)
- `src/app/(learn)/.../[lessonId]/challenge/[challengeId]/page.tsx` (new)
- `src/app/(learn)/.../[lessonId]/page.tsx` (Practice section)
- `package.json` (+@monaco-editor/react, monaco-editor)

## Requirements Covered

CHAL-01, CHAL-02, CHAL-05, CHAL-06, PLAT-06 (responsive workspace), PLAT-07 (public challenge pages indexable).
