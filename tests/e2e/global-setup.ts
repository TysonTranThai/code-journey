import { execSync } from "node:child_process";

/**
 * Playwright global setup: clear rate-limiter state before the suite runs.
 *
 * The E2E suite registers ~14 accounts from loopback within one hour; without
 * this the per-IP register limit (a real control, kept intact for the app)
 * makes later registrations fail and run-submitting tests 401. Deleting the
 * transient limiter rows is safe — they are fixed-window counters, not data.
 *
 * Best-effort: if Docker/DB infra is down the suite still skips via the
 * per-test /health convention.
 */
export default function globalSetup() {
  try {
    execSync(
      'docker exec codejourney-db psql -U codejourney -d codejourney -c "DELETE FROM rate_limit_events"',
      { stdio: "ignore", timeout: 15_000 },
    );
    console.log("[global-setup] rate-limiter state cleared");
  } catch {
    console.log("[global-setup] could not clear rate-limiter state (infra down? tests will skip)");
  }
}
