const { chromium } = require('playwright');

(async () => {
  // Launch a headless browser
  const browser = await chromium.launch({ headless: true });

  // Create a new page
  const page = await browser.newPage();

  // Navigate to Google
  await page.goto('https://www.google.com');

  // Wait for the search input field to become visible and ready for interaction
  await page.waitForSelector('input[name="q"]', { state: 'visible', timeout: 60000 });

  // Type the search query
  await page.type('input[name="q"]', 'OpenAI');

  // Press Enter to submit the search
  await page.keyboard.press('Enter');

  // Wait for the search results to load
  await page.waitForSelector('h3');

  // Extract and print the titles of the search results
  const searchResults = await page.$$eval('h3', results => results.map(result => result.textContent));
  searchResults.forEach(result => console.log(result));

  // Close the browser
  await browser.close();
})();
