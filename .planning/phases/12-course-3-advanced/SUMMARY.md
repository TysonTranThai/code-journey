# Phase 12 — Course 3: Web Development Advanced (Section 1: Advanced HTML) — SUMMARY

Date: 2026-09-12
Status: **COMPLETE — all gates green (Global gates closed 2026-09-13, see Gating note for the unblock)**
Authoring agent: session independent of the Phase 11 agent; Intermediate audited before starting.

## Decision gate (evidence-based)

Course 2 (Web Development Intermediate) was audited before any Advanced work, not taken
on faith from docs/SUMMARY:

| Gate | Result (independently re-run) |
| --- | --- |
| validate-content.ts | PASS — both courses × both locales (259 + 401 nodes each), EN/VI structures match |
| verify-challenges-i2.mjs | 181/181 (reference passes + wrong fails) |
| verify-challenges.mjs (Beginner regression) | 91/91 |
| typecheck / lint | clean / clean |
| unit + integration | 160/160 (27 files) |
| E2E | 36/36 (mobile 375px, keyboard-only, a11y) |
| production build | PASS — 538 static pages |

Disk measurements: 13 modules, 80 EN + 80 VI lessons, 63 practice sets, 169 practice +
12 checkpoint challenges, prerequisite on Beginner enforced. Time split ≈ 45% practice
/ 54% theory over ≈ 43 h (denser than Beginner's post-revision 38% practice). Scope
genuinely exceeds Beginner (closures→capstone full-stack arc).

**Verdict: Intermediate = COMPLETE. Advanced begun per the decision tree.**

## Research

docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-ADVANCED.md — WHATWG HTML LS, MDN, W3C WAI,
web.dev; Baseline facts verified (Popover GA Jan 2025, Invoker Commands Baseline Jan
2026 → `command`/`commandfor` taught as current). Scope decisions documented with
out-of-scope rationale (no constraint-validation re-teach — Intermediate owns it; no
Web Components yet — needs Advanced JS first).

## Delivered (measured on disk)

Course: `web-development-advanced` (track web-development; prerequisite
`web-development-intermediate` enforced; EN + VI course overlays).

Module `advanced-html` — 7 lessons (EN `.mdx` + `.vi.mdx` + metadata + VI overlays):

1. html-architecture — heading outline, hgroup, labelled regions, nested articles
2. accessible-names — name computation, aria-labelledby vs aria-label, ARIA first rule
3. native-disclosure-dialogs — `<details name>`, `<dialog>`, `::backdrop`, autofocus, `method="dialog"`
4. popovers-invokers — popover flavors, `popovertarget`, `command`/`commandfor`
5. responsive-media — srcset/sizes, `<picture>` art direction + format fallback, `fetchpriority`, captions
6. sandboxed-embeds-metadata — iframe `sandbox` token model, Permissions Policy, canonical/OG/hreflang/robots/`<time>`
7. docs-hub-project — project brief (Documentation Hub for "Kite CLI")

7 practice sets / 21 challenges (EN + VI overlays, shared grading code):

- Levels: 7 guided → 6 independent → 4 debugging → 1 real-world + 3 real-world project checkpoints
- Project graded via 3 decision-verification challenges (document+architecture / interactive+media / enhancement+metadata) — cannot be gamed; checks read the artifact
- Every set anchored `afterLesson` (Learn → Practice interleaved; no theory walls)

Tooling:

- scripts/content-authoring/verify-challenges-c3.mjs + c3-solutions.mjs — Course 3 harness
- scripts/content-authoring/validate-c3.ts — Course 3-scoped schema validator (runs while other tracks are mid-authoring)
- validate-content.ts COURSES list extended to include web-development-advanced (one-line, additive)
- track.json / track.vi.json registered Course 3 (additive; VI description extended)

## Verification (this session)

| Gate | Result |
| --- | --- |
| verify-challenges-c3.mjs | **21/21** (reference passes + wrong fails; 3 content/test defects found & fixed during authoring) |
| validate-c3.ts | PASS — 1 module / 7 lessons / 7 sets / 21 challenges, EN/VI parity OK, all zod-validated |
| typecheck | PASS (after `pnpm content:map` → 286 lesson imports incl. Course 3) |
| Beginner harness regression | 91/91 |
| Intermediate harness regression | 181/181 |
| lint | my files clean; 3 warnings exist in scripts/content-authoring/verify-challenges-py.mjs — another agent's in-flight file, left untouched |
| validate-content.ts | **PASS** — 3 courses × 2 locales (incl. advanced: 44 nodes per locale, EN/VI sync OK); python track loads after manifest completion (below) |
| unit + integration | **160/160** (27 files; curriculum-shape assertions updated 136→143 lessons, 1→2 tracks) |
| E2E | **36/36** (mobile 375px, keyboard-only, a11y) |
| production build | **PASS — 694 static pages** (up from 538: Course 3 + Python content) |

Time split for the module: ≈ 86 min theory / ≈ 175 min practice → **≈ 67% hands-on**.

## Gating note (multi-agent) — how the global gates were closed

Midway through this session, a second agent began authoring a **Python track**
(`src/content/tracks/python/...`) in the same working tree. During that window any
full-curriculum load threw (`module reference "python-and-your-first-programs" has
no file …`), blocking `validate-content.ts`, 22 unit tests (all one signature,
none related to Course 3), E2E, and `pnpm build`. Their files were left untouched
while polling for completion.

The agent later went quiet with the tree still unloadable. Root cause: their
`pypb_m1..m7.py` generators write lessons/practices but never call `write_module`,
and `pypb_course.py` leaves `course.json.modules` as `[]` ("filled by module
scripts in order") — that final wiring step was simply never executed.

**Completion (user-authorized "complete all of the rest"):**
- `scripts/content-authoring/pypb_finish_manifests.py` — emits the 7 missing
  `module.json`/`module.vi.json` manifests **using their own `pypb.write_module`
  helper**, with lesson/practice order parsed from their `m*.py` call sites and
  filtered to files that exist on disk (post-`_fix_` state respected); fills
  `course.json.modules` with the 7 module ids. No generated content was clobbered;
  their generator scripts were NOT re-run (that would have discarded their
  `_fix_*.py` patches and duplicated solution entries).
- 3 Python challenge files carried `level` values outside the 7-value
  `practiceLevelSchema` enum; `level` is optional in the schema, so the invalid
  keys were stripped (no grading behavior changed).
- `tests/unit` curriculum-shape assertions updated for the legitimate growth:
  136 → 143 linear web lessons; 1 → 2 tracks (web-development + python);
  web-development course list now [beginner, intermediate, advanced].
- `validate-c3.ts` tightened (no `any`) after lint widened its coverage.

Final gate: typecheck ✓ · lint 0 errors (3 warnings remain in the other agent's
WIP `verify-challenges-py.mjs`, untouched) · validator 3 courses × 2 locales ✓ ·
harnesses 21/21 + 181/181 + 91/91 ✓ · unit 160/160 ✓ · E2E 36/36 ✓ · build 694 ✓

## Leftovers / next steps

- Python track: `verify-challenges-py.mjs` still does not run (imports a missing
  `src/workers/python-runtime` module) and 7th-module practices were authored before
  module manifests existed — their pipeline is the owner; Python completion/QA is
  that agent's phase, not Phase 12.
- The Python course `course.json` carries extra keys (`estimatedMinutes`,
  `nextCourse`) tolerated by the loader's passthrough but not in the zod schema.
- Future Course 3 sections (per research doc): Advanced CSS, Advanced JavaScript,
  Advanced TypeScript, Frontend Architecture — each with its own practice ladder and
  project.
