'''
this does not work right now
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
    page.wait_for_timeout(10000)

    # search for something
    page.fill("textarea", "Playwright Python tutorial")
    page.keyboard.press("Enter")
    
    # wait for page to load and specifically for search results
    page.wait_for_load_state("networkidle")

    # timeout for 10 seconds
    page.wait_for_timeout(10000)

    # wait for div id search
    page.wait_for_selector("div[id='search']")

    # Use a more specific selector for actual search result links
    links = page.query_selector_all("div[id='search'] div.g div.yuRUbf > a")
    for link in links:
        print(link.text_content())
        print(link.get_attribute("href"))
        print("---")
    
    # note down html
    html = page.content()
    with open("data/gitignored/google_search_results.html", "w") as f:
        f.write(html)
    
    # Keep the browser window open until user input
    input("Press Enter to close the browser...")
    browser.close()
    