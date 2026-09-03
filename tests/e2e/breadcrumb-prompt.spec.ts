import { expect, test } from "@playwright/test";

/**
 * Content-presentation E2E (07-09, CURR-01/CURR-03): challenge breadcrumbs
 * show human-readable course/module titles (not slugs), and authored
 * `inline code` in prompts renders as <code>, never literal backticks.
 */
test.skip(process.env.CJ_SKIP_E2E === "1", "E2E explicitly skipped");

const CHALLENGE =
  "/learn/web-development/web-development-foundations/html-foundations/introduction-to-html/challenge/fix-the-heading";

test("breadcrumb shows course and module titles, not slugs", async ({ page }) => {
  await page.goto(CHALLENGE);
  const nav = page.getByRole("navigation", { name: "Breadcrumb" });
  await expect(nav).toBeVisible();
  // Human-readable titles present:
  await expect(nav.getByText("Web Development Foundations")).toBeVisible();
  await expect(nav.getByText("HTML Foundations")).toBeVisible();
  // Raw slugs absent:
  await expect(nav.getByText("web-development-foundations")).toHaveCount(0);
  await expect(nav.getByText("html-foundations")).toHaveCount(0);
});

test("prompt renders inline code spans without literal backticks", async ({ page }) => {
  await page.goto(CHALLENGE);
  const code = page.locator("p code", { hasText: "My First Page" });
  await expect(code).toBeVisible();
  // The instruction paragraph itself contains no literal backtick characters.
  const promptText = await page.locator("p.whitespace-pre-wrap").first().textContent();
  expect(promptText).not.toContain("`");
});

test("authored angle brackets in prompt text stay escaped (no markup injection)", async ({
  page,
}) => {
  await page.goto(CHALLENGE);
  // "uses an <h1> element" is authored with angle brackets; it must render
  // as visible text, not become a DOM element inside the prompt paragraph.
  const promptParagraph = page.locator("p.whitespace-pre-wrap").first();
  await expect(promptParagraph).toBeVisible();
  expect(await promptParagraph.locator("h1").count()).toBe(0);
  expect(await promptParagraph.locator("img").count()).toBe(0);
  expect(await promptParagraph.locator("script").count()).toBe(0);
});
