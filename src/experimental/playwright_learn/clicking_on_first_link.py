'''
Script to search Google and click on the first search result
'''

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

    # search for something
    page.fill("textarea", "Playwright Python tutorial")
    page.keyboard.press("Enter")
    
    # Wait for search results to load
    page.wait_for_load_state("networkidle")
    
    # Get all search result headings
    search_results = page.query_selector_all("div[id='search'] h3")
    
    if search_results:
        print(f"Found {len(search_results)} search results:")
        for result in search_results:
            print(f"- {result.inner_text()}")
        # click on the second result
        search_results[1].click()
    else:
        print("No search results found")
    
    # Keep the browser window open until user input
    input("Press Enter to close the browser...")
    browser.close()
    