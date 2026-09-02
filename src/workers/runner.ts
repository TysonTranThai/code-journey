/**
 * Runner worker (03-CONTEXT D-04). A standalone Node process — started with
 * `pnpm worker` — that polls the Postgres execution queue and runs student
 * code in the sandbox.
 *
 * This is the ONLY process in the system that executes student code. The web
 * tier never spawns interpreters (PLAT-08). In production this process moves
 * to a separate host with its own Docker socket and no user-data credentials.
 *
 * Never logs payload code, env vars, or secrets — only job ids and statuses.
 */
import { closeDb } from "@/lib/db";
import { claimJob, completeJob, failJob, markRunning, requeueStale } from "@/lib/execution/queue";
import { truncateOutput, type VerdictPayload } from "@/lib/execution/types";

// Injected execute hook: real container execution lands in 03-02; tests can
// pass their own. Default = stub that returns an error verdict.
let executeFn: (payload: {
  code: string;
  testFiles: { name: string; code: string }[];
  timeoutMs: number;
  memoryMb: number;
}) => Promise<VerdictPayload> = async () => ({
  verdict: "error",
  perTestResults: [],
  runtimeMs: null,
  output: "runner not implemented (03-02 pending)",
});

/** Test/ops hook: replace the execute implementation. */
export function setExecuteFn(fn: typeof executeFn): void {
  executeFn = fn;
}

const POLL_INTERVAL_MS = Number(process.env.POLL_INTERVAL_MS ?? 1000);
const WORKER_ID = `runner-${process.pid}`;

let running = true;

function shutdown(signal: string) {
  console.log(`[runner] received ${signal} — finishing current job, then exiting`);
  running = false;
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));

async function processOneJob(): Promise<boolean> {
  const job = await claimJob(WORKER_ID);
  if (!job) return false;

  try {
    await markRunning(job.id);
    const verdict = await executeFn(job.payload);
    await completeJob(job.id, {
      ...verdict,
      output: truncateOutput(verdict.output),
    });
    console.log(`[runner] job ${job.id} completed: ${verdict.verdict}`);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    await failJob(job.id, message.slice(0, 500));
    console.error(`[runner] job ${job.id} failed: ${message}`);
  }
  return true;
}

async function main() {
  console.log(`[runner] worker ${WORKER_ID} polling every ${POLL_INTERVAL_MS}ms`);
  while (running) {
    try {
      await requeueStale();
      // Drain as long as jobs are available (latency win), then idle-poll.
      let processed = false;
      do {
        processed = await processOneJob();
      } while (processed && running);
    } catch (err) {
      // Keep the worker alive on transient DB errors; log job-id-free.
      console.error("[runner] loop error:", err instanceof Error ? err.message : err);
    }
    if (!running) break;
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  }
  console.log("[runner] exiting cleanly");
}

main()
  .then(async () => {
    await closeDb();
    process.exit(0);
  })
  .catch(async (err) => {
    console.error("[runner] fatal:", err);
    await closeDb().catch(() => undefined);
    process.exit(1);
  });
