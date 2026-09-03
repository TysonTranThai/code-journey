# Production Execution Architecture

> Scope: this document describes the target architecture and the beta-safe
> boundary implemented in Phase 7. Production infrastructure is **not**
> deployed in Phase 7; the Judge0 migration is a later phase (07-10 decision,
> 2026-09-03).

## Environment split

| Environment      | Execution                                    | Host placement                                                                 |
| ---------------- | -------------------------------------------- | ------------------------------------------------------------------------------ |
| **Local dev**    | Hardened Docker runner (`src/workers/sandbox.ts`) | Developer machine; local Docker daemon (default `SANDBOX_DOCKER_HOST` unset)   |
| **Private beta** | Hardened Docker runner (same code)           | **Dedicated sandbox worker host** via `SANDBOX_DOCKER_HOST` — never the web-tier daemon |
| **Public prod**  | **Self-hosted Judge0** behind the execution queue | Dedicated Judge0 host, isolated from web app, primary DB, and all secrets       |

## Why the web tier must never hold the Docker socket

The sandbox worker spawns `docker run …`. Docker socket access is effectively
**host-root**: a sandbox escape or a worker compromise grants control of
whichever daemon it talks to. Consequences, enforced in Phase 7:

- The web application host runs **no** Docker workload and holds **no**
  Docker socket. It only enqueues jobs (Postgres queue) and reads verdicts.
- In private beta the worker runs on its own host and targets the sandbox
  daemon via `SANDBOX_DOCKER_HOST` (docker `-H`). That endpoint is trusted,
  dedicated, network-restricted to the worker, and never public.
- The worker carries **no user-data credentials** (no app DB user, no auth
  secrets). Its queue access is scoped to the job tables only.

Request path (all environments):

```
Browser → Web App (Next.js) → Postgres queue (execution_jobs)
        → Sandbox Worker (dedicated host in beta) → hardened container
        → verdict written back to Postgres → polled by the browser
```

## Container hardening set (local + beta, verified by tests)

`--network none` · `--read-only` + tmpfs scratch · `--memory` = `--memory-swap`
(no swap) · `--cpus 0.5` · `--pids-limit 64` · `--cap-drop ALL` ·
`--security-opt no-new-privileges` · non-root `--user sandbox` · `--rm` ·
host-side wall-clock kill · 256 KB output caps · per-job random heredoc
delimiter (grade integrity, 07-01).

Unit tests: `tests/unit/sandbox-args.test.ts`.
Isolation suite (real containers): `tests/integration/sandbox-isolation.test.ts`.

## Public production: self-hosted Judge0 requirements

Judge0 does **not** make execution secure by itself. The production host must
satisfy **all** of (07-10 checklist):

1. Host isolation — Judge0 on its own host/microVM; no app DB, no secrets.
2. Network isolation — no egress for executed code; Judge0 API reachable only
   from the worker.
3. CPU + memory limits per submission (cgroups/`setrlimit`), OOM kill.
4. Process limits — PID/fd caps against fork bombs.
5. Wall-clock + CPU timeouts → explicit timeout verdict.
6. Output caps on stdout/stderr.
7. Filesystem isolation — ephemeral root, tmpfs scratch, nothing mounted.
8. Sandbox backend chosen deliberately (Firecracker microVM or gVisor) and
   justified in the deployment doc.
9. Privilege dropping — non-root, dropped caps, `no-new-privileges`.
10. Secret isolation — submitted code never sees env/secrets.
11. No reachability from executed code to Postgres or internal services.
12. Job cleanup — containers/microVMs always torn down.
13. Queue abuse controls — rate limits + concurrency caps (07-03 limiter).
14. Bounded execution concurrency on the host.
15. Monitoring + alerting on job lifecycle, failures, abuse patterns.
16. Failure handling — crashes map to explicit verdicts, never silent hangs.
17. Stale-job reclamation (worker death) with attempts cap.
18. Result integrity — verdicts written server-side only (07-01 holds).

The worker's execution seam (`src/workers/execute.ts`) keeps the typed
`JobPayload`/verdict interface; the Judge0 adapter implements the same
signature, so the swap is contained.

## Operational runbook (beta)

- **Worker up?** `pgrep -f "pnpm worker"`; log shows `worker polling`.
- **Queue stuck?** Check `execution_jobs` rows with old `created_at` and
  `status='queued'`; restart the worker; jobs are re-claimed or fail loudly.
- **Daemon unreachable?** Runs fail with an explicit error verdict; the API
  surfaces "Could not start the run" — never a silent hang.
- **Rotate/patch the sandbox image** on the sandbox host only; the web tier
  is untouched.

## Deferred decisions (honest status)

- Judge0 host provisioning, image choice, and the Firecracker/gVisor backend
  decision: **PLANNED** (later phase).
- Real email provider, CSP/security headers, backups, connection pooling:
  **PLANNED** (docs/SECURITY.md).
