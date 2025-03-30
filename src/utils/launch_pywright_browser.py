from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def launch_pywright_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,  # Make browser visible
        args=['--start-maximized']  # Start with maximized window
    )
    context = await browser.new_context(
        viewport=None,  # Remove viewport size restrictions
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    await stealth_async(page)
    
    print("Browser launched successfully!")  # Debug message
    return playwright, browser, page