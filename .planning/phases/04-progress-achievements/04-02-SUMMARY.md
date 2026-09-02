---
phase: 04-progress-achievements
plan: 02
---

# Plan 04-02 Report: Learner Dashboard

**Completed:** 2026-09-02

## What Was Built

1. **Dashboard projection** (`src/lib/progress/dashboard.ts`): read-only `getDashboardData(userId)` — overall percent (completed lessons+challenges ÷ content totals), per-track percentages, derived streak, achievements grid (earned w/ awardedAt + locked), and continue-learning target (first incomplete linear lesson, deep-linked to its first un-passed challenge when present). No write paths.
2. **Dashboard page** (`src/app/(learn)/dashboard/page.tsx`): server-rendered, authenticated-only (redirect /login), noIndexMetadata, greeting + streak badge, semantic progressbars (role=progressbar with aria-valuenow/min/max), per-track cards, achievements grid, continue-learning card. Responsive: 1 → 2 → 3 column grid (PLAT-06).
3. **Header**: Dashboard link for signed-in users (desktop nav + mobile menu), filtered client-side from server-derived session.
4. **Privacy tests**: dashboard absent from sitemap; no-index metadata asserted (PLAT-07).

## Live-Bug Found and Fixed (session user id)

End-to-end verification exposed a REAL auth bug: the JWT callback stored `role` but never `id`, so `session.user.id` was undefined for every authenticated user — the dashboard redirected even logged-in users, and any progress attribution would have failed. Fixed in `src/lib/auth/config.ts` (persist `token.id`, map to `session.user.id`) + `src/types/next-auth.d.ts` (id typed on Session.user and JWT).

## Verification (live, production build)

- Anonymous GET /dashboard → 307 → /login; authenticated → 200 with noindex header
- Login → pass challenge via API → **progress_event recorded** (`challenge/fix-the-heading`) → **first-challenge achievement awarded** → dashboard renders "Code Runner" earned + locked items + streak + continue-learning link
- Forged POST /api/progress/lesson without session → **401** (PROG-02)
- Gates: typecheck 0 errors, lint clean, format clean, **tests 78/78**, build green

## Files

- `src/lib/progress/dashboard.ts` (new), `src/app/(learn)/dashboard/page.tsx` (new)
- `src/components/layout/SiteHeaderClient.tsx` (Dashboard link)
- `src/lib/auth/config.ts` + `src/types/next-auth.d.ts` (session id fix)
- `tests/unit/dashboard-projection.test.ts` (new)

## Requirements Covered

PROG-01 (completion state visible), PROG-03 (streak display), PROG-04 (achievements display), PLAT-06 (responsive), PLAT-07 (no-index private page).
