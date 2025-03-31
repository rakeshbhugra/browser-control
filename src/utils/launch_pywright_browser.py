from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import os
from urllib.parse import urlparse

async def launch_pywright_browser(use_proxy=False):
    playwright = await async_playwright().start()
    
    if use_proxy:
        proxy_url = os.getenv("PROXY_URL")
        parsed_url = urlparse(proxy_url)
        proxy_server = f"{parsed_url.scheme}://{parsed_url.netloc}"
        proxy_username = parsed_url.username
        proxy_password = parsed_url.password
        proxy = {
            "server": proxy_server,
            "username": proxy_username,
            "password": proxy_password,
        }
    else:
        proxy = None
    
    
    browser = await playwright.chromium.launch(
        headless=False,  # Make browser visible
        args=['--start-maximized'],  # Start with maximized window
        proxy=proxy
    )
    context = await browser.new_context(
        viewport=None,  # Remove viewport size restrictions
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    await stealth_async(page)
    
    print("Browser launched successfully!")  # Debug message
    return playwright, browser, page