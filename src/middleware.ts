import { NextResponse } from "next/server";

/**
 * Security headers (Phase 9 — private beta deployment hardening).
 *
 * Applied to every response so even a forgotten route is protected. Chosen to
 * be safe with the current app (verified against the production build):
 *  - The app embeds no iframes, so frame denial is safe.
 *  - Next.js injects inline scripts (RSC payload/bootstrapping), so CSP
 *    script-src allows 'unsafe-inline' (documented beta limitation); all
 *    other sources are locked to 'self'.
 *  - Development additionally allows 'unsafe-eval': React's dev build needs
 *    eval() for its debugging tooling (call-stack reconstruction). React
 *    never uses eval in production, so the prod policy stays strict.
 *  - HSTS is production-only so local HTTP testing is never poisoned.
 */
const HSTS_VALUE = "max-age=31536000; includeSubDomains";

function buildCsp(isProd: boolean): string {
  const scriptSrc = isProd
    ? "script-src 'self' 'unsafe-inline'"
    : "script-src 'self' 'unsafe-inline' 'unsafe-eval'";
  return [
    "default-src 'self'",
    scriptSrc,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: blob:",
    "font-src 'self' data:",
    "connect-src 'self'",
    "worker-src 'self' blob:",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "object-src 'none'",
  ].join("; ");
}

export function middleware() {
  const isProd = process.env.NODE_ENV === "production";

  const response = NextResponse.next();
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("Content-Security-Policy", buildCsp(isProd));
  if (isProd) {
    response.headers.set("Strict-Transport-Security", HSTS_VALUE);
  }
  return response;
}

export const config = {
  // All routes except hashed static assets and the image optimizer.
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
