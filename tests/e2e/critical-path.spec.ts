import { expect, test } from "@playwright/test";

/**
 * Critical-path E2E (PLAT-03): the full student journey against real infra.
 * Skips when the DB/sandbox infra is unreachable — same convention as the
 * integration suites.
 */

let dbUp = false;
test.beforeAll(async ({ request }) => {
  const res = await request.get("/health");
  const body = (await res.json()) as { db?: string };
  dbUp = body.db === "up";
  test.skip(!dbUp, "Database not reachable — skipping infra-dependent E2E");
});

const uniqueId = () => `e2e-${Date.now()}-${Math.floor(Math.random() * 10_000)}`;

async function register(page: import("@playwright/test").Page, name: string) {
  const id = uniqueId();
  const email = `${id}@e2e.codejourney.local`;
  await page.goto("/register");
  await page.getByLabel(/name/i).fill(name);
  await page.getByLabel(/email/i).fill(email);
  await page
    .getByLabel(/^password/i, { exact: false })
    .first()
    .fill("e2e-password-123");
  await page.getByRole("button", { name: /sign up|create/i }).click();
  await page.waitForTimeout(2000);
  return email;
}

async function solveChallenge(page: import("@playwright/test").Page) {
  // Monaco's visible view-lines intercept pointer events; clicking one focuses
  // the editor like a real user. Select-all is platform-aware via Meta/Control.
  await page.locator(".monaco-editor .view-line").first().click();
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.insertText("<h1>My First Page</h1>");
  await page.getByRole("button", { name: /submit/i }).click();
  // First run in a session pays the sandbox container cold start inside the
  // worker, so allow a generous window before declaring the verdict missing.
  // The banner renders in the aria-live status region AND the output panel.
  await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
    timeout: 75_000,
  });
}

test("critical path: register → browse → run challenge → verdict → dashboard", async ({ page }) => {
  const id = uniqueId();

  // Register (auto signs in).
  await register(page, `E2E ${id}`);

  // Browse: learn index → lesson.
  await page.goto("/learn");
  await expect(page.getByText(/web development/i).first()).toBeVisible();
  await page.goto(
    "/learn/web-development/web-development-beginner/html-foundations/introduction-to-html",
  );
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();

  // Practice hub from the lesson's callout, then the challenge.
  await page
    .getByRole("link", { name: /practice/i })
    .first()
    .click();
  await expect(page).toHaveURL(/practice\/introduction-to-html-practice$/);
  await page
    .getByRole("link", { name: /fix the broken heading/i })
    .first()
    .click();
  await expect(page).toHaveURL(/practice\/introduction-to-html-practice\/fix-the-heading/);

  await solveChallenge(page);

  // Dashboard reflects the verified progress + achievement.
  await page.goto("/dashboard");
  await expect(page.getByText(/overall progress/i)).toBeVisible();
  await expect(page.getByText(/code runner/i).first()).toBeVisible();
});

test("critical path: keyboard-only run reaches the verdict panel", async ({ page }) => {
  const id = uniqueId();
  await register(page, `Kbd ${id}`);

  await page.goto(
    "/learn/web-development/web-development-beginner/html-foundations/practice/introduction-to-html-practice/fix-the-heading",
  );
  await page.locator(".monaco-editor .view-line").first().click();
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.insertText("<h1>My First Page</h1>");
  // Keyboard-only activation: focus Run, press Enter.
  await page.getByRole("button", { name: /submit/i }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
    timeout: 75_000,
  });
});
