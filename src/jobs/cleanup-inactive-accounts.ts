/**
 * Inactive-account cleanup job (non-interactive, cron-friendly).
 *
 * Policy: an account whose last qualifying activity is strictly older than
 * INACTIVE_ACCOUNT_DAYS (default 7) days is deleted. Conservative by design:
 *   - NULL lastActiveAt  → never deleted (no confidently-known activity).
 *   - role='admin'       → never deleted.
 *   - exactly at the boundary (age == threshold) → kept ("more than 7 days"
 *     means strictly older than the threshold).
 *   - all user-owned tables use ON DELETE CASCADE, and the deletion runs in
 *     a single transaction, so there is never partial deletion.
 *
 * Usage:
 *   node --import tsx --import ./scripts/worker-imports.mjs src/jobs/cleanup-inactive-accounts.ts [--dry-run]
 *
 * Environment:
 *   DATABASE_URL             required
 *   INACTIVE_ACCOUNT_DAYS    default 7 (must be a positive number)
 *   DRY_RUN                  "1"/"true" also forces dry-run
 *
 * Exit codes: 0 ok (including "dry-run found eligible accounts"), 1 failure.
 */
import { closeDb } from "@/lib/db";
import { cleanupInactiveAccounts } from "@/lib/maintenance/inactive-accounts";
import { logEvent } from "@/lib/observability";

async function main() {
  const args = process.argv.slice(2);
  const flagDryRun = args.includes("--dry-run") || args.includes("-n");
  const envDryRun = /^(1|true)$/i.test(process.env.DRY_RUN ?? "");
  const dryRun = flagDryRun || envDryRun;

  const result = await cleanupInactiveAccounts({ dryRun });
  logEvent("cleanup.inactive-accounts", "cleanup run finished", { ...result });
  // Machine-readable single-line summary for log pipelines.
  console.log(
    `inactive-account-cleanup: mode=${dryRun ? "dry-run" : "apply"} scanned=${result.scanned} eligible=${result.eligible} deleted=${result.deleted} skipped=${result.skipped} errors=${result.errors} thresholdDays=${result.thresholdDays}`,
  );
  await closeDb();
  process.exit(result.errors > 0 ? 1 : 0);
}

main().catch(async (err) => {
  console.error("inactive-account-cleanup: FAILED", err instanceof Error ? err.message : err);
  try {
    await closeDb();
  } catch {
    // ignore
  }
  process.exit(1);
});
