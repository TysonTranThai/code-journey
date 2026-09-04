import { expect, test } from "@playwright/test";

/**
 * Static public delivery E2E (07-08, PLAT-06/PLAT-07): public content is
 * readable by anonymous visitors (server-rendered HTML, no client-side gate)
 * and the header correctly reflects signed-in state after hydration.
 */
test.skip(process.env.CJ_SKIP_E2E === "1", "E2E explicitly skipped");

const LESSON =
  "/learn/web-development/web-development-beginner/html-foundations/introduction-to-html";

test("public pages render full content for anonymous visitors", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();

  await page.goto("/learn");
  await expect(page.getByText(/web development/i).first()).toBeVisible();

  await page.goto(LESSON);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/html/i);
  await expect(page.getByText(/practice/i).first()).toBeVisible();
});

test("lesson HTML contains server-rendered body content (static, SEO-readable)", async ({
  page,
}) => {
  await page.goto(LESSON, { waitUntil: "domcontentloaded" });
  // The server response must already contain the H1 (not client-injected).
  const h1 = await page.locator("h1").first().elementHandle();
  expect(h1).not.toBeNull();
  const serverHtml = await page.content();
  expect(serverHtml).toContain("Introduction to HTML");
});

test("header shows signed-out actions for anonymous visitors", async ({ page }) => {
  await page.goto("/learn");
  await expect(page.getByRole("link", { name: "Log in" }).first()).toBeVisible();
  await expect(page.getByRole("link", { name: "Sign up" }).first()).toBeVisible();
});
