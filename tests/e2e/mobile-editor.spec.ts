import { expect, test } from "@playwright/test";

/**
 * Mobile/tablet editor render (07-06): the deterministic proof that Monaco
 * exists, is non-zero, paints, accepts input, preserves the draft, and the
 * challenge loop completes. Parameterized across the audit's viewport matrix —
 * widths ≥1024px use the desktop grid (no tabs), narrower widths the tabbed
 * layout. Skips without infra — same convention as the integration suites.
 */

const VIEWPORTS = [
  { width: 1440, height: 900 },
  { width: 1280, height: 800 },
  { width: 1024, height: 768 },
  { width: 768, height: 1024 },
  { width: 430, height: 932 },
  { width: 390, height: 844 },
  { width: 375, height: 667 },
];

let dbUp = false;
test.beforeAll(async ({ request }) => {
  const res = await request.get("/health");
  const body = (await res.json()) as { db?: string };
  dbUp = body.db === "up";
  test.skip(!dbUp, "Database not reachable — skipping infra-dependent E2E");
});

const CHALLENGE_URL =
  "/learn/web-development/web-development-beginner/html-foundations/introduction-to-html/challenge/fix-the-heading";

async function register(page: import("@playwright/test").Page) {
  const id = `e2e-m-${Date.now()}-${Math.floor(Math.random() * 10_000)}`;
  await page.goto("/register");
  await page.getByLabel(/name/i).fill(`Mobile ${id}`);
  await page.getByLabel(/email/i).fill(`${id}@e2e.codejourney.local`);
  await page
    .getByLabel(/^password/i, { exact: false })
    .first()
    .fill("e2e-password-123");
  await page.getByRole("button", { name: /sign up|create/i }).click();
  await page.waitForTimeout(2000);
}

for (const viewport of VIEWPORTS) {
  test(`editor renders and accepts input at ${viewport.width}px`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await register(page);
    await page.goto(CHALLENGE_URL);

    const tabbed = viewport.width < 1024; // lg breakpoint
    if (tabbed) {
      await page.getByRole("tab", { name: "Code" }).click();
    }

    // 07-06: the editor must exist with non-zero, painted dimensions.
    const editorBox = page.locator(".monaco-editor").first();
    await expect(editorBox).toBeVisible();
    const dims = await editorBox.boundingBox();
    expect(dims, "editor bounding box must be non-zero").not.toBeNull();
    expect(dims!.width, "editor width").toBeGreaterThan(50);
    expect(dims!.height, "editor height").toBeGreaterThan(50);

    // Accepts keyboard input.
    await page.locator(".monaco-editor .view-line").first().click();
    await page.keyboard.press("ControlOrMeta+a");
    await page.keyboard.insertText("<h1>Viewport Probe</h1>");
    await expect(page.locator(".monaco-editor").first()).toContainText("Viewport Probe");

    // Draft preservation across tab switches (tabbed layout only).
    if (tabbed) {
      await page.getByRole("tab", { name: "Instructions" }).click();
      await page.getByRole("tab", { name: "Code" }).click();
      await expect(page.locator(".monaco-editor").first()).toContainText("Viewport Probe");
    }
  });
}

test("mobile challenge loop completes: type → run → verdict", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await register(page);
  await page.goto(CHALLENGE_URL);

  await page.getByRole("tab", { name: "Code" }).click();
  await page.locator(".monaco-editor .view-line").first().click();
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.insertText("<h1>My First Page</h1>");

  // 07-07: Run must be reachable from the Code tab via the sticky action bar.
  await page.getByRole("button", { name: /run code/i }).click();
  await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
    timeout: 75_000,
  });
});
