# Plan 02-04 Summary: Curriculum Browsing UI + SEO Surface

**Date:** 2026-09-02 · **Status:** Complete · All verification green

## What Was Built

- **Routes** (`src/app/(learn)/`): `/learn` (tracks) → `/learn/[trackId]` (course grid) → `/learn/[trackId]/[courseId]` (module sections + lesson lists) → `/learn/[trackId]/[courseId]/[moduleId]/[lessonId]` (lesson). Note: the lesson route needs all FOUR segments (fixed from a 3-segment mistake that 404'd in the smoke test).
- **MDX rendering**: `mdx-map.ts` static imports; `@next/mdx@16.3.4` with a serializable config (Turbopack rejects plugin-function options — remark-gfm/rehype-slug installed but not wired; documented in next.config.ts); `mdx-components.tsx` with dark-theme element styling; `src/types/mdx.d.ts`; `@mdx-js/loader` peer added.
- **Header/footer**: `SiteHeader` (server) reads the session server-side (PLAT-08) and renders `SiteHeaderClient` (client island): responsive nav, auth-aware right side, accessible mobile disclosure menu (`aria-expanded`/`aria-controls`), logout via server action (AUTH-04). Integrated in root layout; skip link preserved; `metadataBase` set.
- **Lesson page**: breadcrumbs (aria-label, aria-current), h1, difficulty badge + minutes + "Lesson N of M", MDX body, prev/next pager crossing module boundaries (getLinearNeighbors), "Course complete 🎉" edge state.
- **PLAT-07 SEO**: `generateMetadata` + canonical URLs on public pages; `sitemap.ts` (9 URLs from loaders); `robots.ts` (allow /, disallow /api/, sitemap pointer); no-index auth pages via `noIndexMetadata`.
- **Landing page**: CTA now "Start learning →" (/learn) + direct link to HTML Foundations; honest status text.

## Verification (all run)

| Check | Result |
|---|---|
| `pnpm build` | ✓ 16 static pages, all routes present |
| Lesson page | ✓ h1 "Introduction to HTML" renders, canonical link present |
| Pager | ✓ "Course complete" edge state on last lesson |
| robots.txt via curl | ✓ Allow /, Disallow /api/, Sitemap pointer |
| sitemap.xml via curl | ✓ 9 URLs (/, /learn, track, course, 5 lessons) |
| /login noindex via curl | ✓ `<meta name="robots" content="noindex, nofollow">` |
| **Live auth flow via curl** | ✓ CSRF → login (302) → session JSON `{user:{...role:"student"}}` → personalized header ("Dev Student") → wrong password rejected (session null) → signout → session null |
| `pnpm typecheck` / `lint` / `test` | ✓ / 0 problems / 41/41 |
| `pnpm format:check` | ✓ |

## Bugs Found & Fixed During Verification

1. **AUTH_SECRET missing** → live 500 on all /api/auth endpoints in production mode. Fixed: dev secret generated into `.env.local` (git-ignored). Lesson: `.env.example` placeholders aren't enough for prod-mode smoke tests.
2. **Lesson route segments** → page was at 3 segment levels, URLs use 4. Fixed by moving the page under `[moduleId]`.
3. **`@mdx-js/loader` missing peer** + **non-serializable MDX options** under Turbopack — both fixed (install + empty options object).

## Notes

- Pages render dynamically (ƒ) because the header reads the session in the root layout — crawlable SSR HTML either way. Per-route SSG re-splitting (header as PPR island or client fetch) deferred to Phase 6 performance work.
- Deferred: GFM plugin wiring (needs programmatic MDX compile), JSON-LD, mobile viewport screenshot pass.
