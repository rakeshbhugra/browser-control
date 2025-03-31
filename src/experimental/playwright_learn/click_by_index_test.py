import asyncio
from playwright.async_api import async_playwright
from src.experimental.playwright_learn.click_by_index import highlight_page, get_element_info, click_element, fill_input, remove_highlights
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
        
        # Get information about all elements
        print("\nGetting information about elements:")
        element_count = await page.evaluate("window.highlightedElements.length")
        for i in range(element_count):
            info = await get_element_info(page, i)
            if info:
                print(f"\nElement {i}:")
                for key, value in info.items():
                    if value is not None:  # Only print non-null values
                        print(f"  {key}: {value}")
        
        
        await page.get_by_label('Check-in date').click()
        
        while True:
            print("\nWhat would you like to do?")
            print("1. Click an element")
            print("2. Fill text into an input")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                element_index = int(input("\nEnter the index of the element you want to click: "))
                success = await click_element(page, element_index)
                if success:
                    print(f"Successfully clicked element {element_index}")
                else:
                    print(f"Failed to click element {element_index}")
            
            elif choice == "2":
                element_index = int(input("\nEnter the index of the input element: "))
                text = input("Enter the text to fill: ")
                success = await fill_input(page, element_index, text)
                if success:
                    print(f"Successfully filled text into element {element_index}")
                else:
                    print(f"Failed to fill text into element {element_index}")
            
            elif choice == "3":
                break
            
            else:
                print("Invalid choice. Please try again.")
            

        
        # Remove highlights when done
        await remove_highlights(page)
        
        input("\nPress Enter to close the browser...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 