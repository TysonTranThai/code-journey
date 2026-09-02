import "server-only";

import type { VerdictPayload } from "@/lib/execution/types";

/**
 * Execute-hook seam for the runner worker (03-01).
 *
 * 03-02 replaces this stub with the real hardened-container execution
 * (src/workers/execute.ts imports sandbox.ts). The worker loop depends only
 * on this signature, so the queue backbone is fully testable before the
 * sandbox lands.
 */
export type ExecuteFn = (payload: {
  code: string;
  testFiles: { name: string; code: string }[];
  timeoutMs: number;
  memoryMb: number;
}) => Promise<VerdictPayload>;

export const stubExecute: ExecuteFn = async () => ({
  verdict: "error",
  perTestResults: [],
  runtimeMs: null,
  output: "runner not implemented (03-02 pending)",
});
