import { expect, test } from "@playwright/test";

/**
 * Mobile run flow (07-07): the sticky action bar keeps Run reachable from
 * every tab, announces state via aria-live, and can jump to Output after a
 * verdict. Skips without infra — same convention as the integration suites.
 */

let dbUp = false;
test.beforeAll(async ({ request }) => {
  const res = await request.get("/health");
  const body = (await res.json()) as { db?: string };
  dbUp = body.db === "up";
  test.skip(!dbUp, "Database not reachable — skipping infra-dependent E2E");
});

const CHALLENGE_URL =
  "/learn/web-development/web-development-beginner/html-foundations/practice/introduction-to-html-practice/fix-the-heading";

async function register(page: import("@playwright/test").Page) {
  const id = `e2e-f-${Date.now()}-${Math.floor(Math.random() * 10_000)}`;
  await page.goto("/register");
  await page.getByLabel(/name/i).fill(`Flow ${id}`);
  await page.getByLabel(/email/i).fill(`${id}@e2e.codejourney.local`);
  await page
    .getByLabel(/^password/i, { exact: false })
    .first()
    .fill("e2e-password-123");
  await page.getByRole("button", { name: /sign up|create/i }).click();
  await page.waitForTimeout(2000);
}

test.use({ viewport: { width: 390, height: 844 } });

test("run is reachable from the Code tab without switching", async ({ page }) => {
  await register(page);
  await page.goto(CHALLENGE_URL);

  await page.getByRole("tab", { name: "Code" }).click();
  const runButton = page.getByRole("button", { name: /submit/i });
  await expect(runButton).toBeVisible();

  // Sticky bar stays visible while the instructions scroll.
  const bar = page.getByLabel("Challenge actions");
  await expect(bar).toBeAttached();
  const barBox = await bar.boundingBox();
  const viewportHeight = 844;
  expect(barBox, "action bar in lower viewport").not.toBeNull();
  expect(barBox!.y + barBox!.height).toBeLessThanOrEqual(viewportHeight + 1);
});

test("run from Code tab reaches the verdict and View results jumps to Output", async ({ page }) => {
  await register(page);
  await page.goto(CHALLENGE_URL);

  await page.getByRole("tab", { name: "Code" }).click();
  await page.locator(".monaco-editor .view-line").first().click();
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.insertText("<h1>My First Page</h1>");

  await page.getByRole("button", { name: /submit/i }).click();

  // aria-live status announces completion…
  await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
    timeout: 75_000,
  });
  // …and the bar's View results action switches to the Output tab.
  await page.getByRole("button", { name: /view results/i }).click();
  await expect(page.getByRole("tab", { name: "Output" })).toHaveAttribute("aria-selected", "true");
  await expect(page.getByText(/all tests passed/i).first()).toBeVisible();
});

test("action bar run is keyboard operable", async ({ page }) => {
  await register(page);
  await page.goto(CHALLENGE_URL);

  await page.getByRole("tab", { name: "Code" }).click();
  await page.locator(".monaco-editor .view-line").first().click();
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.insertText("<h1>My First Page</h1>");

  await page.getByRole("button", { name: /submit/i }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
    timeout: 75_000,
  });
});
