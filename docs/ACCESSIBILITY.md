# Accessibility

**Standard:** WCAG 2.1 AA is a product requirement for every learner-facing surface,
established at foundation level and enforced phase by phase. Accessibility retrofits
cost more than building it in — so it is part of the definition of done, not a
follow-up task.

## Requirements (platform-wide)

| Requirement           | Detail                                                                                                               | Status                                             |
| --------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Skip link             | "Skip to main content" as the first focusable element on every page                                                  | IMPLEMENTED in root layout                         |
| Semantic landmarks    | `<header>`, `<nav aria-label>`, `<main id>`, `<footer>` on all pages                                                 | IMPLEMENTED (scaffold); required for all new pages |
| Keyboard navigation   | Every interactive element reachable and operable by keyboard alone; logical tab order                                | REQUIRED from Phase 2 onward                       |
| Visible focus states  | Consistent `:focus-visible` ring (2px, indigo, 2px offset) — never removed                                           | IMPLEMENTED in globals.css                         |
| Color contrast        | Text ≥ 4.5:1 (≥ 3:1 large text) against its background, all themes                                                   | REQUIRED (verified Phase 6)                        |
| Screen reader support | Meaningful labels, `alt` text, live regions for async results (grading, mentor replies)                              | REQUIRED from Phase 3                              |
| Accessible forms      | Labels bound to inputs, errors announced via `aria-describedby`/`aria-live`                                          | REQUIRED from Phase 2                              |
| Reduced motion        | `prefers-reduced-motion: reduce` disables animations/transitions globally                                            | IMPLEMENTED in globals.css                         |
| Readable typography   | Base ≥ 16px, line-height ≥ 1.5, no text below 12px, spacing aids scanning                                            | REQUIRED (verified Phase 6)                        |
| Responsive targets    | Touch targets ≥ 44×44px; layouts usable from 360px width to desktop                                                  | REQUIRED (verified Phase 6)                        |
| Editor accessibility  | The code editor must have a keyboard-navigable, screen-reader-announced alternative path or documented equivalent UX | Phase 3 design requirement                         |
| Automated checks      | axe-based linting in E2E (Phase 6) plus manual keyboard/SR passes each phase                                         | Phase 6                                            |

## Testing Approach

1. **Automated:** eslint jsx-a11y rules (via Next.js config) today; axe checks in the
   Playwright suite (Phase 6).
2. **Manual per phase:** keyboard-only walkthrough of every new flow; VoiceOver/Safari
   spot checks on macOS; contrast verification for new color tokens.
3. **Definition of done:** a feature is not complete with open accessibility
   regressions.
