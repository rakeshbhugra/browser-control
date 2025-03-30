from playwright.sync_api import sync_playwright
import time
import os
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # keep headless=False to handle CAPTCHA
        page = browser.new_page()

        # 1. Go to Google
        page.goto("https://www.google.com")

        # 2. Search for something
        search_query = "Playwright Python tutorial"
        page.fill("textarea", search_query)
        page.keyboard.press("Enter")

        # 3. Wait for navigation and take a screenshot
        page.wait_for_load_state("networkidle")
        os.makedirs("data/gitignored", exist_ok=True)
        page.screenshot(path="data/gitignored/search_result.png")

        browser.close()

if __name__ == "__main__":
    run()
