# Security

**Status as of 2026-09-02 (foundation phase).** This document is deliberately honest:
it separates what is IMPLEMENTED, what is PLANNED, and what is NOT YET VERIFIED.
Nothing here should be read as "secure" until the corresponding verification exists.

## Implemented (verified in this phase)

| Control                | Detail                                                                                                                       |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Secret hygiene in git  | `.gitignore` excludes `.env`, `.env.local`, and all `.env.*local*` variants; only `.env.example` (placeholders) is committed |
| No secrets in code     | No credentials exist in the repository; the app currently requires none                                                      |
| Strict TypeScript      | `strict: true` + `noUncheckedIndexedAccess` — removes a class of undefined-behavior bugs                                     |
| Health endpoint        | `/health` returns only non-sensitive status JSON (no env dumping)                                                            |
| Minimal attack surface | No auth, no DB, no user input handling yet — intentionally nothing to exploit in the scaffold                                |

## Planned (architecture committed, implementation pending)

| Area                        | Plan                                                                                                                                                                                                                                                                                                                                                              | Phase |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| Sandboxed code execution    | Isolated containers (Judge0-style hardening baseline): **no network**, read-only root FS + tmpfs scratch, non-root user, CPU/memory/PID limits, wall-clock timeouts, process caps, ephemeral filesystem. Isolation technology (hardened Docker vs gVisor vs Firecracker microVMs vs self-hosted Judge0) decided at Phase 3 planning against the deployment target | 3     |
| Grading isolation           | Student code reaches execution only via queue → runner worker; the web tier never spawns interpreters                                                                                                                                                                                                                                                             | 3     |
| Malicious-sample test suite | Fork bombs, network egress attempts, filesystem escapes, infinite loops, memory bombs — all must be contained or time out                                                                                                                                                                                                                                         | 3     |
| Authentication              | Auth.js-pattern sessions (httpOnly, secure, rotating), CSRF-safe by design, password hashing via the framework's vetted primitive, email verification + reset, OAuth (GitHub)                                                                                                                                                                                     | 2     |
| Input validation            | Zod schemas at every trust boundary (API routes, content loaders)                                                                                                                                                                                                                                                                                                 | 2+    |
| XSS posture                 | React auto-escaping; MDX content restricted to repo-reviewed files; user-generated HTML sanitized when discussions land                                                                                                                                                                                                                                           | 2/5   |
| SQL injection               | Parameterized queries exclusively via Drizzle; no string-built SQL                                                                                                                                                                                                                                                                                                | 2     |
| SSRF                        | Outbound requests from the app are allow-listed (AI adapter, webhooks); sandbox has no network at all                                                                                                                                                                                                                                                             | 3/5   |
| Rate limiting / abuse       | Per-user limits on submissions, mentor requests, auth attempts                                                                                                                                                                                                                                                                                                    | 3/5   |
| File uploads                | Deferred entirely until a design exists (type/size allowlist, AV scan, storage isolation)                                                                                                                                                                                                                                                                         | v1.x+ |
| Dependency audit            | `pnpm audit` in CI-equivalent checks; triage policy in CONTRIBUTING                                                                                                                                                                                                                                                                                               | 6     |

## Not Yet Verified (explicit)

- **Sandbox escape resistance** — untested until the Phase 3 isolation test suite runs.
  Until then, no claim of execution security is made, and no untrusted code is executed
  anywhere in this codebase.
- **Auth/session security** — no authentication exists yet to verify.
- **CSRF/SSRF posture** — no state-changing endpoints exist yet.
- **Production infrastructure security** — not applicable; nothing is deployed.

## Reporting

Security issues: open a private security advisory (do not open public issues for
exploitable behavior).
