---
phase: 03-challenge-loop-sandbox-execution
plan: 02
---

# Plan 03-02 Report: Hardened Container Sandbox + Isolation Suite

**Completed:** 2026-09-02

## What Was Built

1. **Pinned sandbox image** — `docker/Dockerfile.sandbox` (`codejourney-sandbox:latest` via `pnpm sandbox:build`): node:22.17.0-alpine3.22 (pinned, never `:latest`), non-root `sandbox` user, minimal env, no default CMD. Built and verified locally.
2. **Docker run wrapper** — `src/workers/sandbox.ts`: EVERY student-code run goes through `runSandboxed()` with the full hardening set from the plan: `--network none`, `--read-only` rootfs, `--tmpfs /tmp` and `/job` (16 MB, noexec/nosuid/nodev), `--memory` + `--memory-swap` (hard ceiling, no swap), `--cpus 0.5`, `--pids-limit 64` (fork-bomb containment), `--cap-drop ALL`, `--security-opt no-new-privileges`, `--user sandbox`, `--rm` (ephemeral). Wall-clock timeout enforced by the runner via SIGKILL. Clean environment (PATH/HOME only — no secrets inherit).
3. **Job materialization** — student code + test files are streamed via stdin as a POSIX sh script using quoted heredocs (NO shell expansion — code is data, never interpreted by sh); tests run sequentially with a machine-readable `__TEST_RESULT__ <name> status=<n>` marker per test.
4. **Real executor** — `src/workers/execute.ts`: maps container output to the typed verdict model (`timeout` → educational infinite-loop message; per-test parse; crash-before-tests → `error` with compiler output; failing tests carry the challenge's educational hint — CHAL-05). Wired as the worker's default executor (stub still overridable for tests).
5. **Isolation suite** — `tests/integration/sandbox-isolation.test.ts` (Docker-gated, skips cleanly when Docker is down):
   - fork bomb → contained (pids-limit)
   - network egress probe → NETWORK-BLOCKED
   - filesystem escape attempts (/etc, /usr, /home) → all rejected (WROTE:none)
   - infinite loop → killed at wall-clock timeout
   - memory bomb → terminated by cgroup OOM killer (marker status=137)
   - plus 2 normal-operation tests (all-pass flow, failing-test educational message)

## Security Honesty (docs/SECURITY.md rule)

Hard gate PASSED: all malicious samples contained or timed out (7/7). This supports the claim "hardened per OWASP Docker baseline and verified against the phase's attack classes". It does NOT claim production-grade security — external review + production evolution (Judge0/Firecracker paths) remain documented.

## Verification

- `pnpm typecheck` — 0 errors; `pnpm lint` — clean; `pnpm test` — **59/59** (7 new isolation/operation tests, Docker-gated)
- Sandbox live probe: correct solution → per-test status=0 markers; wrong solution → status=1 + hint on stderr

## Files

- `docker/Dockerfile.sandbox` (new)
- `src/workers/sandbox.ts` (new), `src/workers/execute.ts` (new), `src/workers/runner.ts` (executor wiring)
- `package.json` (+`sandbox:build` script)
- `tests/integration/sandbox-isolation.test.ts` (new)

## Requirements Covered

CHAL-04 (sandboxed execution: no network, resource limits, timeout, non-root, ephemeral fs), CHAL-05 (educational failure output), PLAT-08 (execution only in the worker's sandbox).
