import asyncio
from playwright.async_api import async_playwright
from src.experimental.playwright_learn.highlight_learn import highlight_page, remove_highlights
import base64

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to a page
        await page.goto('https://booking.com')
        
        # Add highlights
        screenshot_base64 = await highlight_page(page)

        # Decode base64 string to bytes and save to file
        screenshot_bytes = base64.b64decode(screenshot_base64)
        with open("screenshot.png", "wb") as f:
            f.write(screenshot_bytes)

        # Remove highlights when done
        # await remove_highlights(page)

        input("Press Enter to continue...")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())