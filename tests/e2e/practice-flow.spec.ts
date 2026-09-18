import { expect, test } from "@playwright/test";

/**
 * Practice-set learner flow (Course 1 revision): the hub communicates the
 * concept, difficulty, level climb, and per-challenge progress; the practice
 * challenge reuses the standard editor/run/verdict flow. Runs on desktop and
 * mobile viewports; skips without infra — same convention as the other suites.
 */

const MINIMAL_DOCUMENT = [
  "<!DOCTYPE html>",
  '<html lang="en">',
  '<head><meta charset="UTF-8"><title>My first page</title></head>',
  "<body>",
  "  <h1>Hello, web</h1>",
  "  <p>I am writing HTML.</p>",
  "</body>",
  "</html>",
].join("\n");

const PRACTICE_HUB =
  "/learn/web-development/web-development-beginner/html-foundations/practice/html-structure-practice";
const PRACTICE_CHALLENGE_URL = `${PRACTICE_HUB}/practice-minimal-document`;

/**
 * Reveal the code editor. Wide layouts render the editor beside the
 * instructions (no tabs after hydration); narrow layouts hide it behind a
 * Code tab. The server HTML always contains tabs, so settle for hydration
 * first to avoid clicking an element the client replaces.
 */
async function openCodeEditor(page: import("@playwright/test").Page) {
  await page.waitForTimeout(1_500);
  const codeTab = page.getByRole("tab", { name: "Code" });
  if (await codeTab.isVisible().catch(() => false)) {
    await codeTab.click();
  }
  await page.locator(".monaco-editor").first().waitFor({ state: "visible", timeout: 30_000 });
}

let dbUp = false;
test.beforeAll(async ({ request }) => {
  test.setTimeout(300_000); // the hook warms Turbopack's cold compile below
  const res = await request.get("/health");
  const body = (await res.json()) as { db?: string };
  dbUp = body.db === "up";
  test.skip(!dbUp, "Database not reachable — skipping infra-dependent E2E");

  // Turbopack's first dev compile of the practice challenge page can exceed
  // the per-test timeout (with a transient dev-only RangeError); warm the
  // route with retries so the run-flow tests exercise the app, not the
  // compiler. Production builds are unaffected.
  const deadline = Date.now() + 240_000;
  while (Date.now() < deadline) {
    const warm = await request.get(PRACTICE_CHALLENGE_URL).catch(() => null);
    if (warm?.ok()) break;
    await new Promise((resolve) => setTimeout(resolve, 5_000));
  }
});

async function register(page: import("@playwright/test").Page) {
  const id = `e2e-p-${Date.now()}-${Math.floor(Math.random() * 10_000)}`;
  await page.goto("/register");
  await page.getByLabel(/name/i).fill(`Practice ${id}`);
  await page.getByLabel(/email/i).fill(`${id}@e2e.codejourney.local`);
  const invite = process.env.E2E_INVITE_CODE;
  if (invite) {
    await page.getByLabel(/invite code/i).fill(invite);
  }
  await page
    .getByLabel(/^password/i, { exact: false })
    .first()
    .fill("e2e-password-123");
  await page.getByRole("button", { name: /sign up|create/i }).click();
  await page.waitForTimeout(2000);
}

test.describe("practice hub (desktop)", () => {
  test("hub communicates concept, difficulty, and the level climb", async ({ page }) => {
    await page.goto(PRACTICE_HUB);

    await expect(page.getByRole("heading", { level: 1 })).toContainText(/document structure/i);
    await expect(page.getByText(/~\d+ min of coding/i)).toBeVisible();
    await expect(page.getByText(/4 challenges?/i)).toBeVisible();

    // Deliberate-practice levels are visible on the challenge list.
    await expect(page.getByText("Imitation").first()).toBeVisible();
    await expect(page.getByText("Guided").first()).toBeVisible();
    await expect(page.getByText("Mini build").first()).toBeVisible();

    // The anchored lesson is reachable ("Need the concept first?").
    await expect(page.getByRole("link", { name: /re-read the lesson/i })).toBeVisible();
  });

  test("progress bar renders for signed-in learners and challenges are linked", async ({
    page,
  }) => {
    await register(page);
    await page.goto(PRACTICE_HUB);

    const progress = page.getByRole("progressbar");
    await expect(progress).toBeVisible({ timeout: 10_000 });
    await expect(progress).toHaveAccessibleName(/practice progress/i);

    const firstChallenge = page.getByRole("link", { name: /Build a Minimal Document/i });
    await expect(firstChallenge).toBeVisible();
  });
});

test.describe("practice challenge run flow", () => {
  test("solve a practice challenge end-to-end and see the verdict", async ({ page }) => {
    await register(page);
    await page.goto(PRACTICE_CHALLENGE_URL);

    await openCodeEditor(page);
    await page.locator(".monaco-editor .view-line").first().click();
    await page.keyboard.press("ControlOrMeta+a");
    await page.keyboard.insertText(MINIMAL_DOCUMENT);

    await page.getByRole("button", { name: /submit/i }).click();
    await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
      timeout: 75_000,
    });
  });

  test("a wrong solution fails with an educational hint, not a bare boolean", async ({ page }) => {
    await register(page);
    await page.goto(PRACTICE_CHALLENGE_URL);

    await openCodeEditor(page);
    await page.locator(".monaco-editor .view-line").first().click();
    await page.keyboard.press("ControlOrMeta+a");
    await page.keyboard.insertText("<p>just a paragraph, no structure</p>");

    await page.getByRole("button", { name: /submit/i }).click();
    await expect(page.getByRole("status")).toBeVisible({ timeout: 75_000 });
    // The verdict area names the failing requirement (doctype/html) instead of "Wrong."
    await expect(page.getByText(/doctype/i).first()).toBeVisible({ timeout: 10_000 });
  });
});

test.describe("practice on mobile (390px)", () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test("hub is usable and challenge run flow works on a phone viewport", async ({ page }) => {
    await register(page);
    await page.goto(PRACTICE_HUB);

    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await expect(page.getByRole("progressbar")).toBeVisible({ timeout: 10_000 });

    // Straight into the run flow from the hub.
    await page.getByRole("link", { name: /Build a Minimal Document/i }).click();
    await expect(page).toHaveURL(new RegExp("practice/html-structure-practice/practice-"));

    await openCodeEditor(page);
    const runButton = page.getByRole("button", { name: /submit/i });
    await expect(runButton).toBeVisible();

    await page.locator(".monaco-editor .view-line").first().click();
    await page.keyboard.press("ControlOrMeta+a");
    await page.keyboard.insertText(MINIMAL_DOCUMENT);
    await runButton.click();
    await expect(page.getByRole("status")).toContainText(/all tests passed/i, {
      timeout: 75_000,
    });
  });
});

test.describe("practice is keyboard operable", () => {
  test("hub challenge list is reachable and operable by keyboard", async ({ page }) => {
    await page.goto(PRACTICE_HUB);

    const firstChallenge = page.getByRole("link", { name: /Build a Minimal Document/i });
    await firstChallenge.focus();
    await expect(firstChallenge).toBeFocused();

    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(new RegExp("/practice-minimal-document"));
  });
});
