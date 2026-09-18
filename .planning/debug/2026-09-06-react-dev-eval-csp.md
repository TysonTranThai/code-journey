# Debug: React dev-mode `eval()` CSP violation (2026-09-06) — RESOLVED

## Symptom

Console error on every dev page:

> eval() is not supported in this environment. If this page was served with a
> `Content-Security-Policy` header, make sure that `unsafe-eval` is included.
> React requires eval() in development mode for various debugging features
> like reconstructing callstacks from a different environment.
> React will never use eval() in production mode

## Diagnosis

- `src/middleware.ts` set one static CSP for all modes:
  `script-src 'self' 'unsafe-inline'` — no `'unsafe-eval'`.
- React's **development** build requires `eval()` for its debugging tooling
  (call-stack reconstruction from a different environment). Under the strict
  CSP the eval is blocked, producing the console error and degrading React
  DevTools / overlay diagnostics in dev.
- React's **production** build never uses eval (per the message itself), so
  the strict prod policy was correct and must stay strict.
- Confirmed by inspecting the served header:
  `curl -sI http://localhost:4000/learn | grep content-security-policy`.

## Fix

`src/middleware.ts`: replaced the single static `CSP` string with
`buildCsp(isProd)`:

- dev: `script-src 'self' 'unsafe-inline' 'unsafe-eval'`
- prod: `script-src 'self' 'unsafe-inline'` (unchanged, strict)

The middleware already computed `isProd` for the HSTS split, so the change
reuses that flag. Comment in the file documents why dev needs `'unsafe-eval'`.

## Verification

- Served dev header now includes `'unsafe-eval'` in `script-src` (curl).
- `pnpm typecheck` clean; unit tests 102/102 pass (middleware has no dedicated
  test; header change is covered by the E2E axe suites, which pass).
- Prod build unaffected (verified separately this session: 213 pages, no CSP
  regression — prod script-src unchanged).

## Notes

- This warning also appeared in earlier E2E logs on this machine; same root
  cause (dev-server CSP), not a page-breaking error.
- Beta containers (:3000) run the production build, so they never showed this.
