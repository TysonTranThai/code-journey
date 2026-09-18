# Deployment (Private Beta — Phase 9)

> **This document describes the ACTUAL, verified deployment path** — the commands
> below were executed and verified on 2026-09-04/05. Aspirational infrastructure
> (public production, Judge0) lives in [`PRODUCTION.md`](PRODUCTION.md) and is
> clearly marked there as NOT YET DEPLOYED.
>
> **Current live beta (2026-09-05):** single-host stack on the user-approved dev
> machine, served at **http://localhost:3000 (loopback-only, user decision — the
> ngrok tunnel was stood down after tunnel-based verification passed)**. A real
> domain + reverse proxy remain the target for shared/public beta (see
> external-dependency list at the bottom).

## Verified beta architecture

```
Browser (this machine) ── http://localhost:3000 ──┐
                                                  ▼
        ┌─────────────────────────────┐   (external HTTPS entry point is
        │ BETA WEB HOST               │    NOT configured — see external
        │  web (Next.js, loopback     │    dependencies; an ngrok tunnel was
        │  127.0.0.1:3000 binding)    │    previously used for verification
        └─────────────────────────────┘    and stood down by user decision)
        ┌─────────────────────────────┐        ┌──────────────────────────┐
        │ BETA WEB HOST               │        │ SANDBOX HOST (beta)      │
        │  web    (Next.js, :3000)    │        │  codejourney-sandbox     │
        │  worker (runner)  ──────┐   │        │  containers only; daemon │
        │  db     (Postgres 16)   │   │        │  reachable only from the │
        └─────────────────────────┼───┘        │  worker (private net)    │
                     ▲            │ SANDBOX_   └──────────────────────────┘
                     │            │ DOCKER_HOST
                     └────────────┘
```

- **Web tier**: serves pages/APIs. Holds no Docker socket, never executes student
  code (type-enforced `JobPayload`; verified by `tests/unit/sandbox-args.test.ts`).
- **Worker**: only process that runs student code, via the hardened container
  (`src/workers/sandbox.ts`: no-network, read-only rootfs, memory/CPU/PID caps,
  cap-drop ALL, non-root, wall-clock kill + container kill).
- **Single-host fallback (CURRENT LIVE BETA)**: `worker-singlehost` profile
  mounts the local socket on the user-approved dev machine. The web container
  binds loopback only (127.0.0.1:3000). The two-host split remains the
  production target.
- **Beta access control**: registration requires an invite code when
  `BETA_INVITE_CODE_SHA256` is set (`src/lib/beta/access.ts`). Verified live:
  correct code registers; wrong code creates 0 accounts (server-enforced); the
  E2E suite passes through the tunnel with the code. The plaintext phrase lives
  only in `deploy/.beta-invite-code.txt` (gitignored, mode 600) next to its
  sha-256 in `deploy/.env.production`.

## Verified facts (2026-09-04)

| Item                                                                                                | Status                                                                                                  |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `Dockerfile.web` builds (deps → build → runnable image)                                             | VERIFIED                                                                                                |
| Web container boots and `/health` returns `db: up`                                                  | VERIFIED                                                                                                |
| Worker container polls the queue                                                                    | VERIFIED                                                                                                |
| End-to-end run inside containers: submit → queue → sandbox → verdict `passed` with per-test results | VERIFIED                                                                                                |
| DB backup (`pg_dump -Fc`)                                                                           | VERIFIED (76 KB dump)                                                                                   |
| Restore into a fresh Postgres (`pg_restore`)                                                        | VERIFIED (266 users / 86 submissions / 71 progress events / 14 tables)                                  |
| Migrations apply from scratch (`drizzle-kit migrate`)                                               | VERIFIED (fresh-DB apply fixed 2026-09-05: latent double-PK defect in `achievements`/`progress_events`) |
| Live sandbox leak check after isolation suite + real runs                                           | VERIFIED (0 leaked containers; wall-clock kill now stops the container itself)                          |     | Full E2E suite (30/30) through the PUBLIC HTTPS URL, incl. invite-gated register → run → verdict | VERIFIED 2026-09-05 (`playwright.beta.config.ts` + `BETA_BASE_URL`); tunnel stood down afterwards by user decision — localhost is the serving entry point |
| Wrong invite code registers 0 accounts (live, server-side)                                          | VERIFIED 2026-09-05                                                                                     |
| HTTPS entry point                                                                                   | **NOT ACTIVE** (loopback-only beta by user decision); tunnel path remains verified and documented below |

## One-time host preparation (beta web host)

1. Install Docker + Compose plugin.
2. `git clone <repo> && cd code-journey`
3. Create `deploy/.env.production` (never committed):

   ```sh
   CJ_PG_PASSWORD=$(openssl rand -hex 24)
   AUTH_SECRET=$(openssl rand -base64 32)
   AUTH_URL=https://YOUR-BETA-DOMAIN
   NEXT_PUBLIC_SITE_URL=https://YOUR-BETA-DOMAIN
   BETA_INVITE_CODE_SHA256=$(printf '%s' 'your-invite-phrase' | shasum -a 256 | cut -d' ' -f1)
   # Optional integrations (all degrade gracefully when unset):
   # EMAIL_PROVIDER=smtp SMTP_URL=smtps://... EMAIL_FROM=...
   # GITHUB_CLIENT_ID=... GITHUB_CLIENT_SECRET=...
   # MENTOR_API_KEY=... (mentor degrades to content-hints without it)
   # SANDBOX_DOCKER_HOST=ssh://sandbox-host   (two-host split)
   ```

## Deploy / update runbook

```sh
docker compose -f deploy/beta.yml build web          # build codejourney-web:latest
docker compose -f deploy/beta.yml up -d db           # Postgres
docker compose -f deploy/beta.yml run --rm migrate   # apply migrations (idempotent)
docker compose -f deploy/beta.yml up -d web worker   # app + runner
curl -s http://127.0.0.1:3000/health                 # expect {"status":"ok","db":"up"}
```

Sandbox host (two-host split): build `codejourney-sandbox:latest` there
(`pnpm sandbox:build` or `docker compose -f deploy/sandbox-host.yml build`), then
expose the daemon to the worker ONLY (ssh:// recommended, or read-only TCP bound
to the private interface + firewall — see comments in `deploy/sandbox-host.yml`).

## Backups

```sh
# one-shot
docker compose -f deploy/beta.yml --profile backup run --rm backup
# cron (nightly 03:17, keep 14) — add via crontab -e on the web host
17 3 * * * cd /path/to/code-journey && docker compose -f deploy/beta.yml --profile backup run --rm backup && ls -1t deploy/backups/*.dump | tail -n +15 | xargs -r rm
```

Restore procedure (VERIFIED on 2026-09-04):

```sh
docker run --rm -i --network codejourney_default postgres:16-alpine \
  pg_restore -h db -U codejourney -d codejourney --clean --if-exists --no-owner \
  < deploy/backups/<file>.dump      # PGPASSWORD from env or -e
```

## Rollback

- **App**: previous image tag → `docker tag codejourney-web:latest codejourney-web:bad && git checkout <prev-sha> && docker compose -f deploy/beta.yml build web && docker compose -f deploy/beta.yml up -d web worker`
- **Migrations**: never auto-down-migrate. Restore the pre-migration backup instead (hence backup before every `migrate` run).
- **Broken worker**: `docker compose -f deploy/beta.yml stop worker` — execution degrades to queued jobs (UI already shows honest queue status).
- **Kill-switch**: stop the worker to disable ALL challenge execution instantly without touching the rest of the platform.

## Health & monitoring (beta)

- `/health` — app + DB status JSON (public-safe, no internals).
- Compose healthchecks: `web` (HTTP), `worker` (runner process alive), `db` (`pg_isready`).
- `docker compose -f deploy/beta.yml ps` + `logs worker|web` — job lifecycle, errors, restarts.
- Beta escalation trigger: `web` healthcheck failing > 2 min, or repeated worker restarts.

## External dependencies NOT yet satisfied (honest list)

1. **HTTPS entry point for non-local users** — the beta currently serves only
   this machine (loopback). When testers should reach it remotely, either re-add
   the tunnel (see below) or configure a real domain + reverse proxy (Caddy
   recommended for automatic TLS).
2. **Dedicated sandbox host** — target topology per docs/PRODUCTION.md; the live
   single-host fallback is an accepted private-beta compromise.
3. **Email provider credentials** — SMTP adapter is implemented and env-gated;
   real delivery is UNVERIFIED until credentials exist.
4. **AI mentor key** — optional; NullMentor degradation verified.

## Re-enabling the tunnel (verified procedure, currently stopped)

The tunnel was used and fully verified, then removed at user decision. To serve
non-local testers again:

```sh
docker run -d --name cj-beta-tunnel --network cj-beta_default --restart unless-stopped \
  -v "$HOME/Library/Application Support/ngrok/ngrok.yml:/etc/ngrok/ngrok.yml:ro" \
  -e NGROK_CONFIG=/etc/ngrok/ngrok.yml ngrok/ngrok:3 \
  http cj-beta-web-1:3000 --log stdout --log-format=json
docker logs cj-beta-tunnel 2>&1 | grep -oE '"url":"https://[^"]+'   # get URL
# then set AUTH_URL + NEXT_PUBLIC_SITE_URL in deploy/.env.production to that URL and:
cd deploy && docker compose -f beta.yml --profile singlehost up -d --force-recreate web
docker rm -f cj-beta-tunnel   # to stand it down again (restore loopback URLs + recreate web)
```

---

## PUBLIC PRODUCTION — codejourney.shop (deployed & verified 2026-09-17)

**Live URL:** <https://codejourney.shop> · **Health:** `GET /health` →
`{"status":"ok","db":"up","service":"code-journey",...}` (public-safe, no internals).

### Architecture (verified on the VPS)

```
Internet ── 80/443 (ufw allows only 22/80/443) ──► EXISTING host nginx
                                                    │ TLS termination (certbot,
                                                    │ auto-renew, expires 2026-12-16)
                                                    ▼ proxy_pass
                                          127.0.0.1:3010 (loopback only)
                                                    │
                        ┌───────────────────────────┴──────────────┐
                        │ docker compose -f deploy/prod.yml        │
                        │  db      postgres:16-alpine (volume)     │
                        │  web     Next.js — no Docker socket      │
                        │  worker  runner — ONLY service with the  │
                        │          Docker socket (sandbox runs)    │
                        │  cleanup/migrate/backup — one-shot       │
                        │          profiles, invoked on demand     │
                        └──────────────────────────────────────────┘
```

- Stack name `cj-prod`; the web container publishes **loopback-only**
  `127.0.0.1:3010:3000` — nothing but the host nginx reaches it. App port 3010
  and Postgres are NOT reachable from the internet (ufw verified:
  deny-incoming default, only 22/80/443 open).
- All services `restart: unless-stopped`; Docker is enabled at boot → app
  survives crashes and reboots.
- The worker runs student code exclusively inside the hardened sandbox image
  (`codejourney-sandbox:latest`, built on the VPS); the web tier never touches
  the Docker socket.

### Environment (deploy/.env.production on the VPS — never committed)

Verified variable names (all referenced by the code/compose file):

| Variable | Purpose |
| --- | --- |
| `CJ_PG_PASSWORD` | Postgres password (injected into containers by compose) |
| `AUTH_SECRET` | Auth.js JWT signing secret (generated, 32+ bytes) |
| `AUTH_URL` | `https://codejourney.shop` (cookies/CSRF origin) |
| `NEXT_PUBLIC_SITE_URL` | `https://codejourney.shop` |
| `INACTIVE_ACCOUNT_DAYS` | Inactivity threshold (7 on production) |
| `SANDBOX_IMAGE` | optional; defaults to `codejourney-sandbox:latest` |

### Deploy / update runbook (each command verified 2026-09-17)

```sh
ssh ubuntu@<vps>
cd ~/code-journey
# 1. sync code (rsync the working tree, exclude node_modules/.git/.next)
# 2. build + bring up
docker compose -f deploy/prod.yml --env-file deploy/.env.production build web
docker compose -f deploy/prod.yml --env-file deploy/.env.production up -d db
docker compose -f deploy/prod.yml --env-file deploy/.env.production run --rm migrate   # idempotent
docker compose -f deploy/prod.yml --env-file deploy/.env.production --profile backup run --rm backup   # pre-migration safety
docker compose -f deploy/prod.yml --env-file deploy/.env.production up -d web worker
curl -s http://127.0.0.1:3010/health
```

First-time nginx/TLS setup is scripted and idempotent:
`scripts/deploy-vps-nginx.sh` (HTTP-only server block → `certbot --nginx` →
redirect config, from `deploy/nginx-codejourney.shop.conf`). It ADDS one site
(`codejourney.shop`) and never touches the host's other sites.

### Account activity & 7-day inactivity cleanup

- `users.last_active_at` (migration `0007`, backfilled from verified activity
  evidence: submissions / progress events / comments; NULL = unknown).
- **Qualifying activity** (defined in `src/lib/auth/activity.ts`): any request
  that reads an authenticated session, plus registration (seeds the field so a
  new account starts a fresh 7-day window). Throttled to at most one write per
  user per 5 minutes via a guarded UPDATE (no write inside the window).
- **Eligibility** (`src/lib/maintenance/inactive-accounts.ts`): `role='student'`
  AND `last_active_at` NOT NULL AND strictly older than `INACTIVE_ACCOUNT_DAYS`
  (exactly-7-days-old is KEPT). Admin accounts and NULL-activity accounts are
  never deleted. Deletion is per-user transactional with an in-transaction
  re-check; all dependent rows cascade (accounts, sessions, reset tokens,
  submissions, progress, achievements, discussion posts…).
- **Dry-run first, always**: the compose `cleanup` service hard-codes dry-run;
  apply requires the explicit override below. The nightly cron applies AFTER
  that night's fresh backup.

```sh
# dry-run (default — deletes nothing)
docker compose -f deploy/prod.yml --env-file deploy/.env.production --profile cleanup run --rm cleanup
# apply (explicit override; preceded by a fresh backup in the nightly job)
docker compose -f deploy/prod.yml --env-file deploy/.env.production --profile cleanup run --rm cleanup pnpm cleanup
```

### Nightly ops (cron, appended to ubuntu's crontab — existing entries untouched)

```
47 2 * * * /home/ubuntu/code-journey/scripts/cj-nightly.sh >> …/deploy/logs/cron.log 2>&1
```

`scripts/cj-nightly.sh`: backup (`pg_dump -Fc`, keep 14, prune runs in a
container because dumps are root-owned) → cleanup in APPLY mode. Logs:
`deploy/logs/backup.log`, `deploy/logs/cleanup.log`.

### Backup & restore (restore VERIFIED into a throwaway DB)

```sh
docker compose -f deploy/prod.yml --env-file deploy/.env.production --profile backup run --rm backup
# restore into a THROWAWAY db first (never into the live db):
docker run --rm --network cj-prod_default -e PGPASSWORD="$CJ_PG_PASSWORD" \
  -v "$HOME/code-journey/deploy/backups:/backups:ro" postgres:16-alpine sh -c \
  'createdb -h db -U codejourney cj_restore && pg_restore -h db -U codejourney -d cj_restore --no-owner /backups/<file>.dump'
```

### Edge security (nginx layer, deployed & verified 2026-09-17)

- **X-Forwarded-For is OVERWRITTEN** (`proxy_set_header X-Forwarded-For $remote_addr;`),
  never appended: the app's rate limiter trusts the first XFF entry, so appending
  would let any client spoof fresh IPs and bypass all per-IP limits. No CDN sits
  in front, so `$remote_addr` is authoritative.
- **`cj_auth` zone**: 10 r/IP/s, burst 5 on `POST /api/auth/callback/credentials`
  (credential-stuffing brake before bcrypt CPU is spent) — verified: 17× 429
  among 25 concurrent hits.
- **`cj_general` zone**: 30 r/IP/s, burst 60 on all dynamic routes
  (site-wide flood brake sized for a classroom behind one NAT; immutable
  `/_next/static/` is exempt) — verified: all 200 at classroom burst, 429s
  under flood.
- Zones are installed at `http{}` level as
  `/etc/nginx/conf.d/codejourney-security.conf` (repo:
  `deploy/nginx-codejourney-security.conf`, installed by
  `scripts/deploy-vps-nginx.sh`).
- The nightly job also **prunes expired `rate_limit_events` rows** (bounded
  table size; the table holds visitor IPs and must not be retained forever).

App-level enforcement (unchanged, verified): per-IP register 20/h, login 10/h
+ 5/min burst, reset 5/h; per-user+IP runs 400/day + 12/min; bcrypt cost 12;
`__Host-`/`__Secure-` cookies (HttpOnly, Secure, SameSite=Lax); CSP + HSTS +
X-Frame-Options DENY middleware; owner-only submission verdicts with 404
masking; fresh-from-DB role checks.

### Troubleshooting

- Status: `docker compose -f deploy/prod.yml --env-file deploy/.env.production ps`
  (all three services should be `Up … (healthy)`).
- Logs: `docker compose -f deploy/prod.yml --env-file deploy/.env.production logs web|worker`.
- TLS: `certbot certificates` on the host (auto-renew timer is systemd-managed).
- Worker kill-switch: `docker compose -f deploy/prod.yml --env-file deploy/.env.production stop worker`
  — execution queues instead of failing; UI shows honest queue status.
- Migrations: never down-migrate; restore the pre-migration backup instead.
