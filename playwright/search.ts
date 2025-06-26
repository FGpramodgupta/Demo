import { chromium } from 'playwright';

(async () => {
  const chromePath = 'C:\\Path\\To\\Your\\Chrome\\chrome.exe'; // 👈 Replace with your actual path

  const browser = await chromium.launch({
    headless: false,
    executablePath: chromePath,
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  // Step 1: Go to Google
  await page.goto('https://www.google.com');

  // Accept cookies if shown (for EU or cookie banners)
  const acceptButton = page.locator('button:has-text("Accept all")');
  if (await acceptButton.isVisible()) {
    await acceptButton.click();
  }

  // Step 2: Search for query
  await page.locator('input[name="q"]').fill('Pramod Gupta Indium Software');
  await page.keyboard.press('Enter');

  // Wait for results
  await page.waitForSelector('h3');

  // Step 3: Click the first result link
  const firstResult = page.locator('h3').first();
  await firstResult.click();

  // Optional: Wait a bit before closing
  await page.waitForTimeout(5000);

  await browser.close();
})();
