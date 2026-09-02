/**
 * Vitest stub for the `server-only` guard package. The real package throws
 * when imported outside a React Server Component environment; unit/integration
 * tests run in plain Node via vitest, so it must be neutralized there.
 * The Next.js production build aliases the real package and enforces the
 * guard for real.
 */
export {};
