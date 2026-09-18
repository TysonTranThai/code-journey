/**
 * Production-mode auth lifecycle verification (local rehearsal + prod check).
 * Drives the real HTTP surface (register → session → protected routes →
 * logout → login variants → duplicate registration) against a running
 * Code Journey instance and prints PASS/FAIL per step.
 *
 * Usage: node scripts/verify-auth-lifecycle.mjs <base-url>
 * Disposable test account: cj-deploy-verify-<rand>@example.invalid
 */
const B = process.argv[2] ?? "http://localhost:3457";
const rand = Math.random().toString(36).slice(2, 8);
const EMAIL = `cj-deploy-verify-${rand}@example.invalid`;
const NAME = "CJ Deploy Verify";
const PASS = "correct-horse-battery-9";

let jar = []; // {name, value}
let pass = 0;
let fail = 0;

function check(label, ok, detail = "") {
  if (ok) {
    pass++;
    console.log(`PASS  ${label}${detail ? ` — ${detail}` : ""}`);
  } else {
    fail++;
    console.log(`FAIL  ${label}${detail ? ` — ${detail}` : ""}`);
  }
}

function storeCookies(res) {
  for (const raw of res.headers.getSetCookie?.() ?? []) {
    const [pair] = raw.split(";");
    const eq = pair.indexOf("=");
    const name = pair.slice(0, eq).trim();
    const value = pair.slice(eq + 1).trim();
    const idx = jar.findIndex((c) => c.name === name);
    if (value === "" && idx >= 0) jar.splice(idx, 1);
    else if (idx >= 0) jar[idx] = { name, value };
    else jar.push({ name, value });
  }
}

function cookieHeader() {
  return jar.map((c) => `${c.name}=${c.value}`).join("; ");
}

async function get(path, { redirect = "manual" } = {}) {
  const res = await fetch(`${B}${path}`, {
    redirect,
    headers: { cookie: cookieHeader() },
  });
  storeCookies(res);
  return res;
}

async function postForm(path, fields, { redirect = "manual" } = {}) {
  const body = new URLSearchParams(fields);
  const res = await fetch(`${B}${path}`, {
    method: "POST",
    redirect,
    headers: {
      cookie: cookieHeader(),
      "content-type": "application/x-www-form-urlencoded",
      origin: B,
    },
    body,
  });
  storeCookies(res);
  return res;
}

async function getRegisterPageHiddenFields() {
  const res = await get("/register", { redirect: "follow" });
  const html = await res.text();
  const fields = {};
  const inputRe = /<input[^>]*type="hidden"[^>]*>/g;
  for (const tag of html.match(inputRe) ?? []) {
    const name = tag.match(/name="([^"]*)"/)?.[1];
    const value = tag.match(/value="([^"]*)"/)?.[1];
    if (name) fields[name.replace(/&quot;/g, '"')] = (value ?? "").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
  }
  return fields;
}

async function main() {
  // 1. health
  const health = await get("/health", { redirect: "follow" });
  const healthJson = await health.json();
  check("health endpoint ok + db up", healthJson.status === "ok" && healthJson.db === "up", JSON.stringify(healthJson));

  // 2. registration through the real form (Server Action fields)
  const hidden = await getRegisterPageHiddenFields();
  const csrfRes = await get("/api/auth/csrf", { redirect: "follow" });
  const { csrfToken } = await csrfRes.json();
  const reg = await postForm("/register", {
    ...hidden,
    name: NAME,
    email: EMAIL,
    password: PASS,
    csrfToken,
  });
  const regOk = reg.status === 200 || (reg.status >= 300 && reg.status < 400);
  check("registration accepted (2xx/3xx)", regOk, `status ${reg.status}`);

  // 3. session cookie present
  const hasSession = jar.some((c) => c.name.startsWith("authjs.session-token"));
  check("session cookie set after registration", hasSession);

  // 4. protected route accessible with session
  const learn = await get("/learn", { redirect: "follow" });
  check("protected /learn reachable with session (200)", learn.status === 200, `status ${learn.status}`);

  // 5. protected route blocked when anonymous
  const saved = jar;
  jar = [];
  const dashAnon = await get("/dashboard");
  check("anonymous /dashboard redirected to login", dashAnon.status >= 300 && dashAnon.status < 400 && String(dashAnon.headers.get("location") ?? "").includes("/login"), `status ${dashAnon.status} → ${dashAnon.headers.get("location")}`);
  jar = saved;

  // 6. invalid password rejected
  jar = [];
  const csrf2 = await (await get("/api/auth/csrf", { redirect: "follow" })).json();
  const bad = await postForm("/api/auth/callback/credentials", {
    csrfToken: csrf2.csrfToken,
    email: EMAIL,
    password: "wrong-password-123",
  });
  const badLoc = bad.headers.get("location") ?? "";
  check("invalid password rejected", bad.status === 302 && badLoc.includes("error=CredentialsSignin"), `→ ${badLoc}`);

  // 7. nonexistent account rejected with identical error shape
  const csrf3 = await (await get("/api/auth/csrf", { redirect: "follow" })).json();
  const ghost = await postForm("/api/auth/callback/credentials", {
    csrfToken: csrf3.csrfToken,
    email: `ghost-${rand}@example.invalid`,
    password: "whatever-123456",
  });
  const ghostLoc = ghost.headers.get("location") ?? "";
  check("nonexistent account rejected with same generic error", ghost.status === 302 && ghostLoc.includes("error=CredentialsSignin") && ghostLoc === badLoc, `→ ${ghostLoc}`);

  // 8. valid login (fresh browser)
  const csrf4 = await (await get("/api/auth/csrf", { redirect: "follow" })).json();
  const good = await postForm("/api/auth/callback/credentials", {
    csrfToken: csrf4.csrfToken,
    email: EMAIL,
    password: PASS,
  });
  const goodLoc = good.headers.get("location") ?? "";
  check("valid login succeeds", good.status === 302 && !goodLoc.includes("error"), `→ ${goodLoc}`);
  const hasSession2 = jar.some((c) => c.name.startsWith("authjs.session-token"));
  check("session cookie set after login", hasSession2);
  const learn2 = await get("/learn", { redirect: "follow" });
  check("protected route reachable after re-login", learn2.status === 200, `status ${learn2.status}`);

  // 9. duplicate registration (enumeration-safe, no 2nd account)
  jar = [];
  const hidden2 = await getRegisterPageHiddenFields();
  const csrf5 = await (await get("/api/auth/csrf", { redirect: "follow" })).json();
  const dup = await postForm("/register", {
    ...hidden2,
    name: "Dup",
    email: EMAIL,
    password: "another-pass-12345",
    csrfToken: csrf5.csrfToken,
  });
  const dupHtml = await dup.text();
  const dupSoftError = dupHtml.includes("already") || dupHtml.includes("might");
  check("duplicate registration shows enumeration-safe message", dup.status === 200 && dupSoftError, `status ${dup.status}`);

  // 10. logout
  const csrf6 = await (await get("/api/auth/csrf", { redirect: "follow" })).json();
  const out = await postForm("/api/auth/signout", { csrfToken: csrf6.csrfToken });
  check("logout succeeds", out.status === 302, `status ${out.status}`);
  const dashAfter = await get("/dashboard");
  check("protected route blocked after logout", dashAfter.status >= 300 && dashAfter.status < 400, `status ${dashAfter.status}`);

  console.log(`\nRESULT: ${pass} passed, ${fail} failed${fail > 0 ? " ⚠" : " ✓"}`);
  console.log(`test account: ${EMAIL}`);
  process.exit(fail > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error("verification script crashed:", err);
  process.exit(1);
});
