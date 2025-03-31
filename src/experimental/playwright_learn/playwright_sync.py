from playwright.sync_api import sync_playwright

p = sync_playwright().start()  # Start the Playwright context
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.booking.com")
page.screenshot(path="screenshot.png")

page.locator("input[placeholder='Where are you going?']").fill("Dubai")

page.locator("button", has_text="Check-out date").click()

# browser.close()
# p.stop()  #
