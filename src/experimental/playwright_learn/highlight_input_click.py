from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from src.experimental.playwright_learn.click_by_index import highlight_page, get_element_info
import json
import asyncio
import base64
import os

async def main():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    # await stealth_async(page)
    
    await page.goto("https://www.booking.com")
    await page.wait_for_timeout(1000)
    
    screenshot_base64 = await highlight_page(page)

    os.makedirs("element_info", exist_ok=True)
    
    with open("screenshot.png", "wb") as f:
        f.write(base64.b64decode(screenshot_base64))
    
    # prepare element index json
    element_index = {}
    element_count = await page.evaluate("window.highlightedElements.length")
    for i in range(element_count):
        info = await get_element_info(page, i)
        element_index[i] = {}
        if info:
            for key in sorted(info.keys()):
                value = info[key]
                if value is not None:
                    element_index[i][key] = value
    
    with open("element_index.json", "w") as f:
        json.dump(element_index, f, indent=4)
    
    await page.locator("input[placeholder='Where are you going?']").fill("Dubai")
    await page.locator("button", has_text="Check-out date").click()
    
    await browser.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(main())