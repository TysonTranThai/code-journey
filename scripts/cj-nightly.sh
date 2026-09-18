#!/bin/bash
# Code Journey nightly ops: backup → rate-limit-table prune → inactive-account
# cleanup (apply). Runs ON the VPS via ubuntu's crontab (appended, never
# replacing existing entries).
CJ="$HOME/code-journey"
COMPOSE="docker compose -f $CJ/deploy/prod.yml --env-file $CJ/deploy/.env.production"
LOGDIR="$CJ/deploy/logs"
mkdir -p "$LOGDIR"

# Nightly database backup first, keep the 14 most recent dumps.
$COMPOSE --profile backup run --rm backup >> "$LOGDIR/backup.log" 2>&1
# Dump files are written by the (root-running) backup container, so pruning
# also runs in a container — the invoking user cannot rm them directly.
docker run --rm -v "$CJ/deploy/backups:/backups" alpine sh -c \
  'ls -1t /backups/codejourney-prod-*.dump 2>/dev/null | tail -n +15 | xargs -r rm -f'

# Prune expired rate-limit rows (SECURITY: bounded table size; the table holds
# visitor IPs, so it must not be retained indefinitely).
docker exec cj-prod-db-1 psql -U codejourney -d codejourney -c \
  "DELETE FROM rate_limit_events WHERE expires_at < now();" >> "$LOGDIR/maintenance.log" 2>&1

# Inactive-account cleanup (APPLY) — always preceded by a fresh backup, so
# every destructive run has a same-night recovery point.
$COMPOSE --profile cleanup run --rm cleanup pnpm cleanup >> "$LOGDIR/cleanup.log" 2>&1
