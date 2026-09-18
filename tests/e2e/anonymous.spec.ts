import { expect, test } from "@playwright/test";

/**
 * Anonymous + privacy E2E (COMM-03, PLAT-07): visitors can read everything
 * public; private pages redirect and stay no-index.
 */
test.skip(process.env.CJ_SKIP_E2E === "1", "E2E explicitly skipped");

test("anonymous visitors can read curriculum and challenges", async ({ page }) => {
  await page.goto("/learn");
  await expect(page.getByText(/web development/i).first()).toBeVisible();

  await page.goto(
    "/learn/web-development/web-development-beginner/html-foundations/introduction-to-html",
  );
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByText(/practice/i).first()).toBeVisible();

  await page.goto(
    "/learn/web-development/web-development-beginner/html-foundations/practice/introduction-to-html-practice/fix-the-heading",
  );
  await expect(page.getByRole("button", { name: /submit/i })).toBeVisible();
});

test("anonymous users can open a lesson discussion and read", async ({ page }) => {
  await page.goto(
    "/learn/web-development/web-development-beginner/html-foundations/introduction-to-html/discussion",
  );
  await expect(page.getByText(/ask a question|sign in/i).first()).toBeVisible();
});

test("dashboard redirects anonymous visitors to login", async ({ page }) => {
  await page.goto("/dashboard");
  await expect(page).toHaveURL(/\/login/);
});

test("health endpoint reports DB status", async ({ request }) => {
  const res = await request.get("/health");
  expect(res.ok()).toBe(true);
  const body = (await res.json()) as { status: string; db: string };
  expect(body.status).toBe("ok");
  expect(["up", "down"]).toContain(body.db);
});
