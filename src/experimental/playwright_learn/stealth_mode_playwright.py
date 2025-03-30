
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    stealth_sync(page)
    page.goto("https://www.google.com")
    page.wait_for_timeout(10000)

    # search for something
    page.fill("textarea", "Playwright Python tutorial")
    page.keyboard.press("Enter")
    
    # click on the first result
    page.click("text=Playwright Python tutorial")

    # Keep the browser window open until user input
    input("Press Enter to close the browser...")
    browser.close()
    
    browser.close()