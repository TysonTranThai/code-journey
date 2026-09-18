# Curriculum Research — Web Development Advanced (Course 3)

**Status:** living research doc for Course 3 — Web Development Advanced
**Created:** 2026-09-12 (Advanced HTML section authored against these sources)
**Predecessors:** CURRICULUM-RESEARCH-WEB-DEVELOPMENT-BEGINNER.md (Course 1), CURRICULUM-RESEARCH-WEB-DEVELOPMENT-INTERMEDIATE.md (Course 2)
**Rule applied throughout:** sources inform scope and pedagogy; every explanation and challenge is original Code Journey content. No text, examples, or challenge wording is copied from any source.

---

## 1. Sources consulted

| Source | Used for | Confidence |
| --- | --- | --- |
| WHATWG HTML Living Standard (html.spec.whatwg.org — §4.11 interactive elements, §6.12 popover, §4.8 media, §4.4 content model, §14 common idioms) | Ground truth for `<dialog>`, popover, `<details>`/`<summary>`, media, content-model rules, `<template>` | HIGH |
| MDN Web Docs (HTML reference & guides: responsive images, `<dialog>`, Popover API, Invoker Commands API, `<iframe>`, constraint validation, document metadata, WAI-ARIA basics) | Practical semantics, attribute behavior, browser support notes | HIGH |
| W3C WAI (WAI-ARIA Authoring Practices patterns, Using ARIA, landmark guidance, WCAG 2.1 AA success criteria referenced platform-wide) | Accessibility pedagogy: names/roles/values, landmark strategy, native-first rule | HIGH |
| web.dev (Learn HTML, Learn Images, Learn Accessibility; Baseline blog posts) | Course organization patterns, image authoring practices, feature-availability framing | MEDIUM-HIGH |
| Baseline announcements: Popover API cross-browser GA Jan 2025; Invoker Commands API Baseline Jan 2026 | What may be taught as platform-native in 2026 | MEDIUM-HIGH |
| HTML Living Standard changelog + whatwg/html issues (e.g. #9625 invoker buttons proposal → shipped `command`/`commandfor`) | Distinguishing shipped vs speculative features | HIGH |

Excluded as content sources: paid courses, blog-only hot takes, and framework docs (React/Vue) — Advanced HTML is platform HTML, taught framework-agnostically so it feeds later framework and architecture work instead of depending on any of it.

---

## 2. What "Advanced HTML" means after Beginner + Intermediate

A learner finishing Courses 1–2 can already:

- build complete pages with semantic structural elements (header/nav/main/section/article/aside/footer) and validate clean document skeletons (Beginner);
- use `<form>` with `required`, `type="email"`, `minlength`, `pattern`, read `validity` states, and surface errors with `aria-invalid` + `role="alert"` + `aria-describedby` (Intermediate — constraint validation is *already covered* in `advanced-forms`);
- embed images with meaningful `alt`, links with fragments, tables and lists (Beginner).

Therefore Course 3 must **not** re-teach forms validation, basic semantics, or `alt` text. The genuine advanced-HTML skill set is:

1. **Semantic architecture** — heading order as document architecture (skipping levels, hgroup semantics, sectioning + aria-labelledby, `<article>` nesting semantics), deciding between equivalent-markup alternatives by their *accessibility and machine-readability* consequences.
2. **Accessible names, roles, and states** — computing an element's accessible name (content → alt → aria-label → aria-labelledby priority), `aria-labelledby` vs `aria-label` vs `<label>`, when native semantics win and when ARIA supplements them (ARIA first rule).
3. **Native disclosure & dialogs** — `<details name="">` accordion groups, `<dialog>` with `showModal()`/`show()`/`close()`, `::backdrop`, `autofocus` placement, `aria-labelledby` on dialogs, forms inside dialogs, and the dialog-vs-popover-vs-details decision table.
4. **Popovers and declarative invokers** — `popover`/`popovertarget`/`popovertargetaction`, light dismiss, anchor-free positioning limits, and the 2026-standard `command`/`commandfor` invoker model (Baseline Jan 2026), replacing bespoke JS for disclose/overlay patterns.
5. **Responsive media** — `srcset` with w-descriptors and DPR, `sizes` math, `<picture>` for art direction and format switching (avif/webp/jpeg fallback chains), `fetchpriority`, `decoding`, `loading`, intrinsic `width`/`height` against layout shift, and `<video controls muted playsinline poster>` with `<track kind="captions">`.
6. **Sandboxed embeds** — `iframe sandbox` tokens and their risk model (why `allow-scripts allow-same-origin` together is the dangerous combination), `allow=` (Permissions Policy delegation), `title` for accessible name, `loading="lazy"`, and third-party embed judgment.
7. **Document metadata** — `<meta viewport>` (and interactive-widget), canonical URLs, `robots` at page and element level (`rel="nofollow"`, `<meta name="robots" content="noindex">`), Open Graph/Twitter card concepts, `<link rel="alternate" hreflang>`, `lang`/`dir` correctness, `<time datetime>`, `<address>`, `<abbr>` — machine-readable HTML.
8. **Progressive enhancement** — `<details>`/`<dialog>`/`<form>`/`:target` patterns that *work without JavaScript*, then get enhanced; teaching JS as an enhancement layer on top of meaning (this is the bridge to Advanced JavaScript that follows).

Explicitly **deferred** (later Course 3 sections): Web Components, ARIA deep patterns (combobox/grid/tree), `<template>`/shadow DOM internals, streaming HTML, HTML modules/import maps. Advanced HTML deliberately stops at the platform layer learners can master in one focused module; Web Components deserve their own section built on the JS-architecture knowledge that precedes them in Course 3.

---

## 3. Pedagogy findings carried forward

- **Deliberate practice beats re-reading** (Beginner §9; Intermediate research): every lesson is followed by hands-on practice; time split is engineered, not incidental. Course 3 target: ≥ 45% hands-on minutes.
- **Diagnose-don't-memorize** (Intermediate): performance/audit challenges grade on correct *decisions* about broken artifacts, not on writing prose.
- **Decision-verification for open work** (Intermediate capstone): projects are graded by grading challenges that check structural properties of the artifact — impossible to complete without producing the artifact.
- **Native-first ARIA rule** (WAI-ARIA Authoring Practices, "first rule of ARIA"): prefer native elements; teach ARIA as vocabulary for understanding names/roles/states, not as a markup replacement. Challenges reinforce this by *failing* submissions that bolt ARIA onto the wrong native element (e.g. `role="button"` on a div where `<button>` is correct).
- **Course 3 progression** (instructions → problems → engineering, per Intermediate): each lesson states *what · why · when · how it works · what goes wrong · how to practice · where it connects to real applications*.

---

## 4. Practice structure for Advanced HTML

Loop used across every lesson (Learn → Practice separation from Phase 10 is preserved):

1. guided — reproduce the pattern with the learner's own content, graded on structure;
2. independent — no template to imitate, requirements only;
3. debugging — a deliberately broken artifact (wrong element, missing accessible name, unsafe iframe, missing fallback format) must be diagnosed and fixed; hints diagnose, they don't reveal;
4. mini-build / real-world — combine several concepts into a component;
5. project — a **Documentation Hub** (knowledge-base article page for an open-source-style tool) integrating everything: landmark + heading architecture, accessible names, native disclosure + dialog, responsive media, sandboxed embed, metadata/social cards, progressive enhancement — graded via decision-verification challenges.

Practice-density budget for the module (measured after authoring — see docs/COURSE-3-WEB-DEVELOPMENT-ADVANCED.md §Practice):

- 6 lessons ≈ 66 min theory
- 6 practice sets / 18 challenges ≈ 150 min hands-on
- → ≈ 69% hands-on, matching the deliberate-practice evidence.

---

## 5. Topic decisions (in / out)

**In:** heading/landmark architecture; accessible names & aria-labelledby; `<details name>`; `<dialog>` + backdrop + autofocus + invoker commands; popover basics; responsive images (srcset/sizes/picture/fetchpriority); video + captions; iframe sandbox/allow/title; metadata (viewport, canonical, robots, OG, hreflang, lang, time).

**Out (with rationale):**
- *Constraint validation API* — already mastered in Intermediate `advanced-forms`; re-teaching would violate the no-redundancy rule. Advanced HTML only *builds* on it (dialog forms).
- *Web Components / `<template>`* — belongs later in Course 3, after Advanced JavaScript architecture; including it here would front-load JS-dependent concepts into an HTML module.
- *ARIA widget patterns (combobox, tree, datagrid)* — specialist territory; this module teaches when NOT to need them.
- *SEO tooling specifics (schema.org microdata end-to-end)* — covered as concepts (OG/structured metadata) here; full structured-data authoring is a future module.
- *Servers-side rendering internals / streaming* — platform-architecture territory for the production section of Course 3.

---

## 6. Vietnamese localization notes

Course name: **Lập trình Web — Nâng cao**; section: **HTML nâng cao**.

Established-translation rules carried from Courses 1–2 (verified against existing `.vi.mdx`/`.vi.json`):

- Keep in English: HTML, DOM, ARIA, API, JavaScript, CSS, `srcset`, `sizes`, `<dialog>`, `popover`, `sandbox`, `viewport`, element/attribute names, code identifiers.
- Natural Vietnamese technical prose for concepts already in the corpus (match Intermediate usage): *khả năng tiếp cận* (accessibility), *HTML ngữ nghĩa* (semantic HTML), *nâng cấp tăng tiến* (progressive enhancement), *bố cục/tài liệu* for structure/landmark phrasing, *tên truy cập được* for accessible name.
- Structural sync: `.vi.json` overlays carry title/prompt/hint translations only; grading `code` is shared — one harness verifies both locales.
