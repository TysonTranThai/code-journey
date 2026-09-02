/**
 * Module-resolution hook for the runner worker (`pnpm worker`): aliases the
 * `server-only` guard package to an empty stub. The worker is a plain Node
 * process that legitimately runs server-side code; Next builds keep the real
 * guard. Loaded via scripts/worker-imports.mjs.
 */
export async function resolve(specifier, context, next) {
  if (specifier === "server-only") {
    return {
      url: "data:text/javascript,export {}",
      shortCircuit: true,
    };
  }
  return next(specifier, context);
}
