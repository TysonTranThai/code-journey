# 2026-09-13 — Vietnamese test names unreadable in verdict panel

**Learner bug report:** a failed JS challenge showed

```
Một số bài kiểm tra chưa đạt
188 ms
❌
l-i-ch-o-ch-nh-x-c
file:///job/test-l-i-ch-o-ch-nh-x-c.mjs:5
```

— diacritics destroyed, plus a raw Node crash-report path as the failure reason. "No one understands it in Vietnamese."

## Root causes (systemic, all 3 runtimes)

1. **`sanitizeName()` in `sandbox.ts`, `python-runtime.ts`, `cpp-runtime.ts`** used `[^a-z0-9-_]` → `-`, shattering every Vietnamese test name (`lỗi chờ chính xác` → `l-i-ch-o-ch-nh-x-c`). Audit: **1,364 of 1,408 localized test names are non-ASCII** — platform-wide impact, not one challenge.
2. **`execute.ts` hint logic** attached Node's uncaught-exception crash report to failing tests: `file:///job/test-….mjs:5` (location line), the echoed source line, caret markers, `at …` frames, and the `Node.js v22.17.0` tail line all became "hints" when a test snippet threw *outside* its try/catch (author snippet bug or parse error).
3. **Verdict panel** displayed the worker's marker id instead of the authoritative locale-correct name from challenge data.

## Fixes

- **`src/workers/sanitize-name.ts` (new, shared)** — diacritic-preserving sanitizer: keeps `\p{L}\p{N}` (Vietnamese letters survive), lowercases ASCII, maps spaces/hyphens safely, collision-suffixes unsafe/overlong names; ASCII names are byte-identical to before (back-compat with every existing marker and harness). Wired into all three runtimes.
- **`src/workers/execute.ts`** — hint-pool filters Node crash-report shapes: `file://` location lines, `at ` stack frames, caret markers, the `Node.js vX.Y.Z` tail, and source-echo lines (keyword/call-start shaped). Real error messages (`ReferenceError: x is not defined`, assertion messages) survive.
- **`VerdictPanel` / `ChallengeWorkspace` / both challenge pages** — pass localized `testNames` from challenge data; the panel shows the locale-correct name per index, falling back to the marker name.

## Verification (all measured live, 2026-09-13)

- `scripts/content-authoring/verify-runtime-vi-names.mjs` — the exact report shape through the **real `executeJob` → `runSandboxed`** path: failing test reports `lỗi-chờ-chính-xác` + hint `chưa chứa lời tạm biệt`; passing test reports `đầu-ra-đúng-định-dạng`; crash-shape test reports `undefined_helper is not defined`. **No `file://`, no `node:internal`, no `Node.js vX` anywhere in the payload.** Exit 0.
- `pnpm typecheck` clean; eslint clean on all 8 touched files.
- C++ Beginner challenge harness re-run: 46/46 two-sided OK (sanitizer rename is byte-compatible).
- Live routes on :3000 (200): `/learn`, `/learn/cpp`, `/sitemap.xml`.

## Known external transient (not this bug)

During verification, 22 unit tests failed — **all** traced to the concurrent C++ Intermediate agent's `cpp-intermediate/course.json` containing `"modules": []` (mid-authoring shell): the strict loader rejects it and the global curriculum load fails for every consumer (unit tests, sitemap building). Not caused by, and not fixable from, this bug-fix scope; it resolves when that agent fills the manifest. Live preview was unaffected at check time.
