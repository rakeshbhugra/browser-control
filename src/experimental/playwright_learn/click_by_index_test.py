import asyncio
from playwright.async_api import async_playwright
from src.experimental.playwright_learn.click_by_index import highlight_page, get_element_info, click_element, remove_highlights
import base64

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to a page
        await page.goto('https://booking.com')
        
        # Add highlights and get screenshot
        screenshot_base64 = await highlight_page(page)
        
        # Save screenshot
        with open("screenshot.png", "wb") as f:
            f.write(base64.b64decode(screenshot_base64))
        
        # Get information about some elements
        print("\nGetting information about elements:")
        for i in range(5):  # Get info for first 5 elements
            info = await get_element_info(page, i)
            if info:
                print(f"\nElement {i}:")
                for key, value in info.items():
                    if value:  # Only print non-null values
                        print(f"  {key}: {value}")
        
        # Wait for user input to see the highlights
        input("\nPress Enter to continue...")
        
        # Example of clicking an element
        element_index = int(input("\nEnter the index of the element you want to click: "))
        success = await click_element(page, element_index)
        if success:
            print(f"Successfully clicked element {element_index}")
        else:
            print(f"Failed to click element {element_index}")
        
        # Remove highlights when done
        await remove_highlights(page)
        
        input("\nPress Enter to close the browser...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 