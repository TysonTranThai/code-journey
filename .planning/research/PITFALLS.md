# Pitfalls Research

**Domain:** Coding education platform (online judge + LMS + community)
**Researched:** 2026-09-02
**Confidence:** MEDIUM-HIGH

## Critical Pitfalls

### Pitfall 1: Running student code without real isolation

**What goes wrong:** "Just for the demo" `eval`/`child_process` on the app server becomes load-bearing forever; one malicious submission exfiltrates DB credentials
**Why it happens:** Sandbox setup feels like a later problem; demo pressure
**How to avoid:** Never execute untrusted code on the web tier — not once, not behind a flag. Graded execution goes through the queue → isolated runner from the very first challenge
**Warning signs:** Any code path where submission bytes reach `eval`, `Function`, `spawn` on the app server
**Phase to address:** Foundation (principle documented now); first execution phase (implementation)

### Pitfall 2: Sandbox that "works" but isn't secure

**What goes wrong:** Container without network isolation, memory/CPU limits, or timeout ceilings; students mine crypto or attack internal services
**Why it happens:** Containers are confused with VMs; defaults are permissive
**How to avoid:** Checklist per execution: no network, read-only FS + tmpfs, PID/CPU/memory limits, wall-clock timeouts, non-root user, seccomp/apparmor profile; treat Judge0-style hardening as the reference
**Warning signs:** Sandbox can reach the database host or internet by default
**Phase to address:** Execution phases; security review before any public launch

### Pitfall 3: Curriculum hardcoded into components

**What goes wrong:** Lessons as JSX → content locked in code; no review workflow; contributors blocked
**Why it happens:** Fast start
**How to avoid:** Content-as-data (MDX/JSON) with zod schema validation at load; build fails on invalid content
**Warning signs:** More than a handful of lessons living in `.tsx` files
**Phase to address:** First curriculum phase

### Pitfall 4: Progress model that can't answer "what's done?"

**What goes wrong:** Boolean flags per lesson scattered everywhere; streaks/certificates/analytics impossible; cheating via client-trusted progress
**Why it happens:** Progress looks simple
**How to avoid:** Single append-friendly progress/completion model derived from server-verified events; UI reads projections
**Warning signs:** Client decides completion state; no server event trail
**Phase to address:** Progress/curriculum phases

### Pitfall 5: AI mentor that does the homework

**What goes wrong:** Students paste challenge → AI returns solution → learning outcome collapses; platform becomes an answer machine
**Why it happens:** Naive system prompts; completion-optimizing models
**How to avoid:** Pedagogical guardrails in the adapter: hint ladders, Socratic responses, refusal policy for full solutions, per-user rate limits; test the guardrails explicitly
**Warning signs:** AI responses contain complete working solutions to current challenges
**Phase to address:** AI mentor phase

### Pitfall 6: Auth bolted on late / misconfigured

**What goes wrong:** Sessions without rotation, missing CSRF posture, OAuth state bugs; migration pain once real users exist
**Why it happens:** Auth is "boring"
**How to avoid:** Adopt Auth.js (or equivalent) patterns at the foundation phase; document dev-only vs production auth posture clearly
**Warning signs:** Custom crypto; secrets in client bundles
**Phase to address:** Auth phase (post-foundation)

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Postgres-backed queue instead of Redis/RabbitMQ | One less infra dependency | Lower throughput ceiling | v1 — absolutely fine |
| Log-file "email" transport in dev | No SMTP needed | None if interface is pluggable | Dev only |
| Single worker process | Simplicity | Grading latency under load | v1 |
| Storing submissions in Postgres | Simple | Table growth | v1; archive to object storage later |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| LLM provider | Streaming tokens straight to client with system prompt leakage | Server-side adapter; sanitize; never ship prompts client-side |
| Monaco editor | Bundling all languages → multi-MB payload | Load lazily per editor use |
| Docker-in-dev | Assuming daemon is running; port conflicts | `docker compose up -d db` gated behind check; use non-conflicting ports (3001/5173 are taken on this machine) |
| Playwright in CI/CI-less envs | Forgetting browser install step | `playwright install` documented as explicit step |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Cold container per execution | 2-10s grading latency | Pool warm containers per language | Day 1 of real users |
| N+1 progress queries | Slow dashboard | Batch queries; projections | ~10k rows |
| Unbounded submission logs | Bloated DB | Retention/truncation policy | Weeks of usage |
| AI calls per keystroke | Cost blowout | Debounce + explicit "ask mentor" actions | Immediate |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Trusting client-sent progress/completion | Fake certificates, corrupted analytics | Server-side verification only |
| Secrets in NEXT_PUBLIC_ vars | Key leakage | Only non-secret values public; audit at build |
| Sandbox shares Docker network with DB | Container escape → DB access | Separate networks; deny by default |
| MDX rendering untrusted content | XSS via plugin pipeline | Only repo-reviewed content; sanitize any user-generated HTML later |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Desktop-only challenges | Mobile learners bounce | Responsive lesson reading on mobile; challenges desktop-first, clearly messaged |
| Error messages that don't teach | Frustration loop | Test-failure output designed for learning (diffs, hints) |
| Losing student code on navigation/refresh | Rage-delete | Persist drafts locally per challenge immediately |

## "Looks Done But Isn't" Checklist

- [ ] **Sandbox:** often missing network denial + timeout ceilings — verify with malicious sample scripts
- [ ] **Auth:** often missing session invalidation on password change
- [ ] **Progress:** often missing server-side verification of completions
- [ ] **Editor:** often missing mobile fallback message and keyboard a11y
- [ ] **AI mentor:** often missing refusal tests for "just solve it" prompts

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Student code ran on app server | HIGH | Rotate all secrets, audit access logs, migrate to isolated runner immediately |
| Hardcoded curriculum | MEDIUM | Extract to content-as-data with codemods |
| Broken progress model | MEDIUM | Rebuild from submission/event history |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Unisolated execution | Foundation (principle) + execution phases | Malicious-sample test suite |
| Insecure sandbox config | Execution phases | Isolation checklist audit |
| Hardcoded curriculum | Curriculum phase | Content schema validation in build |
| Client-trusted progress | Progress phase | Server-verified event test |
| AI auto-solving | AI phase | Guardrail test suite |
| Auth misconfig | Auth phase | Session/CSRF test suite |

## Sources

- Judge0 hardening model (no-network containers, limits) — MEDIUM-HIGH
- freeCodeCamp public post-mortems/practices; OWASP guidance — MEDIUM
- Community post-mortems on online-judge compromises — MEDIUM

---
*Pitfalls research for: Code Journey — free coding education platform*
*Researched: 2026-09-02*
