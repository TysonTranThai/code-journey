#!/usr/bin/env bash
# Phase 9 live verification: production build + worker, security regression
# over HTTP, learner-journey smoke test. Self-contained (tears down at exit).
set -u
cd "$(dirname "$0")/.."

PASS=0; FAIL=0
ok()  { echo "PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
section() { echo ""; echo "=== $1 ==="; }

BETA_HASH=$(printf '%s' 'phase9-beta-invite' | shasum -a 256 | cut -d' ' -f1)
JAR=/tmp/cj9-cookies.txt
LOG_WEB=/tmp/cj9-web.log
LOG_WORKER=/tmp/cj9-worker.log
rm -f "$JAR" "$LOG_WEB" "$LOG_WORKER"

# ── start production server + worker ─────────────────────────────
AUTH_SECRET=phase9-verify-secret AUTH_URL=http://localhost:3000 \
  BETA_INVITE_CODE_SHA256="$BETA_HASH" \
  pnpm start >"$LOG_WEB" 2>&1 &
WEB_PID=$!
for i in $(seq 1 30); do
  curl -sf -m 2 http://localhost:3000/health >/dev/null && break
  sleep 1
done
pnpm worker >"$LOG_WORKER" 2>&1 &
WORKER_PID=$!
sleep 2

shutdown() {
  kill "$WORKER_PID" "$WEB_PID" 2>/dev/null
  pkill -f 'src/workers/runner.ts' 2>/dev/null
}
trap shutdown EXIT

curl_json() { curl -s -m 20 -b "$JAR" -c "$JAR" -H 'Content-Type: application/json' "$@"; }

# ── 1. security headers ──────────────────────────────────────────
section "Security headers"
HDRS=$(curl -sI http://localhost:3000/learn)
echo "$HDRS" | grep -qi 'content-security-policy' && ok "CSP present" || bad "CSP missing"
echo "$HDRS" | grep -qi 'x-content-type-options: *nosniff' && ok "nosniff" || bad "nosniff missing"
echo "$HDRS" | grep -qi 'x-frame-options: *DENY' && ok "frame deny" || bad "frame deny missing"
echo "$HDRS" | grep -qi 'referrer-policy' && ok "referrer-policy" || bad "referrer-policy missing"
echo "$HDRS" | grep -qi 'permissions-policy' && ok "permissions-policy" || bad "permissions-policy missing"

# ── 2. health ────────────────────────────────────────────────────
section "Health"
H=$(curl -s http://localhost:3000/health)
echo "$H" | grep -q '"db":"up"' && ok "health db up" || bad "health: $H"

# ── 3. public curriculum (anonymous) ─────────────────────────────
section "Anonymous curriculum access"
C=$(curl -s http://localhost:3000/learn)
echo "$C" | grep -q 'Web Development' && ok "course listed anonymously" || bad "course missing on /learn"
LP=$(curl -s http://localhost:3000/learn/web-development/web-development-beginner/the-web-and-your-first-website/your-first-html-page)
echo "$LP" | grep -qi 'doctype\|your first' && ok "lesson readable anonymously" || bad "lesson not readable"
CP=$(curl -s http://localhost:3000/learn/web-development/web-development-beginner/the-web-and-your-first-website/your-first-html-page/challenge/build-a-complete-page)
echo "$CP" | grep -q 'Your First Personal Page' && ok "challenge instructions readable anonymously" || bad "challenge page missing"
echo '=== robots/sitemap ==='
curl -s http://localhost:3000/robots.txt | grep -q 'sitemap.xml' && ok "robots + sitemap ref" || bad "robots missing sitemap"
curl -s http://localhost:3000/sitemap.xml | grep -c '<url>' | xargs -I{} echo "sitemap urls: {}"

# ── 4. protected API without session ─────────────────────────────
section "Execution requires auth"
CODE=$(curl -s -o /tmp/cj9-body.json -w '%{http_code}' -X POST http://localhost:3000/api/challenges/run \
  -H 'Content-Type: application/json' \
  -d '{"code":"<h1>x</h1>","trackId":"web-development","courseId":"web-development-beginner","moduleId":"the-web-and-your-first-website","lessonId":"your-first-html-page","challengeId":"build-a-complete-page"}')
[ "$CODE" = "401" ] && ok "anonymous run rejected 401" || bad "anonymous run → $CODE"

# ── 5. registration (beta gate) ──────────────────────────────────
section "Beta gate on the register page"
REG=$(curl -s http://localhost:3000/register)
echo "$REG" | grep -q 'Invite code' && ok "invite-code field present (gate active)" || bad "invite-code field missing"

# ── 6. authenticated run flow (seeded dev-student) ────────────────
section "Learner flow (dev fixture login)"
# credentials sign-in: csrf token then FORM-encoded callback POST
CSRF=$(curl -s -c "$JAR" http://localhost:3000/api/auth/csrf | sed -E 's/.*"csrfToken":"([^"]+)".*/\1/')
LOGIN=$(curl -s -m 20 -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  "http://localhost:3000/api/auth/callback/credentials" \
  --data-urlencode "csrfToken=$CSRF" \
  --data-urlencode "email=dev-student@codejourney.local" \
  --data-urlencode "password=dev-password-123" \
  --data-urlencode "callbackUrl=http://localhost:3000/learn" \
  --data-urlencode "json=true" \
  -o /dev/null -w '%{http_code} %{redirect_url}')
echo "login: $LOGIN"
grep -c 'authjs.session-token' "$JAR" >/dev/null && ok "session cookie issued" || bad "no session cookie in jar"
echo "$LOGIN" | grep -q 'error=' && bad "login redirect contains error" || ok "no auth error in redirect"
curl -s -b "$JAR" http://localhost:3000/api/auth/session | grep -q 'dev-student' && ok "session established" || bad "no session"

SUB=$(curl_json -b "$JAR" -X POST http://localhost:3000/api/challenges/run \
  -d '{"code":"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Me</title></head>\n<body><h1>Kayaking</h1><p>Paddle rivers.</p><p>Build kayaks.</p></body></html>","trackId":"web-development","courseId":"web-development-beginner","moduleId":"the-web-and-your-first-website","lessonId":"your-first-html-page","challengeId":"build-a-complete-page"}')
echo "run response: $SUB"
SUBID=$(echo "$SUB" | sed -E 's/.*"submissionId":"([^"]+)".*/\1/')
[ -n "$SUBID" ] && [ "$SUBID" != "$SUB" ] && ok "run accepted (submission created)" || bad "run not accepted"

# wait for verdict (poll until a terminal verdict arrives)
VERDICT=""
for i in $(seq 1 40); do
  V=$(curl_json -b "$JAR" "http://localhost:3000/api/challenges/run/$SUBID")
  case "$V" in
    *'"status":"queued"'*|*'"status":"claimed"'*|*'"status":"running"'*) sleep 2 ;;
    *)
      VERDICT=$(echo "$V" | sed -E 's/.*"verdict":"([a-z]+)".*/\1/')
      break
      ;;
  esac
done
echo "verdict: $VERDICT"
[ "$VERDICT" = "passed" ] && ok "sandbox verdict: passed" || bad "verdict was: $VERDICT"

# ── 7. IDOR check (no session) ───────────────────────────────────
section "Submission ownership"
CODE2=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:3000/api/challenges/run/$SUBID")
[ "$CODE2" = "401" ] || [ "$CODE2" = "404" ] && ok "anonymous cannot read submission ($CODE2)" || bad "submission readable anonymously: $CODE2"

# ── 8. rate limit (6th run inside a minute → 429) ────────────────
section "Rate limit (burst: 5 runs/min)"
CODE3=000
for i in 1 2 3 4 5 6; do
  CODE3=$(curl -s -o /dev/null -w '%{http_code}' -b "$JAR" -X POST http://localhost:3000/api/challenges/run \
    -H 'Content-Type: application/json' \
    -d '{"code":"<h1>x</h1>","trackId":"web-development","courseId":"web-development-beginner","moduleId":"the-web-and-your-first-website","lessonId":"your-first-html-page","challengeId":"build-a-complete-page"}')
done
[ "$CODE3" = "429" ] && ok "burst limit returns 429 on the 6th run" || bad "expected 429 on 6th run, got $CODE3"

# ── 9. progress persisted ────────────────────────────────────────
section "Progress"
curl -s -b "$JAR" http://localhost:3000/dashboard | grep -qi 'streak\|progress' && ok "dashboard renders" || bad "dashboard missing"

echo ""
echo "=== RESULT: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ]
