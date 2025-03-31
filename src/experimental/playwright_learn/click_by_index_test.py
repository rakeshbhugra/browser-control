import asyncio
from playwright.async_api import async_playwright
from src.experimental.playwright_learn.click_by_index import highlight_page, get_element_info, click_element, fill_input, remove_highlights
import base64
import json
from datetime import datetime
import os

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
        
        # Create directory for element info if it doesn't exist
        os.makedirs("element_info", exist_ok=True)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"element_info/elements_{timestamp}.txt"
        
        # Get information about all elements and write to file
        print(f"\nWriting element information to {filename}")
        element_count = await page.evaluate("window.highlightedElements.length")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Page URL: {page.url}\n")
            f.write(f"Total Elements Found: {element_count}\n")
            f.write("-" * 80 + "\n\n")
            
            for i in range(element_count):
                info = await get_element_info(page, i)
                if info:
                    f.write(f"Element {i}:\n")
                    # Sort keys for consistent output
                    for key in sorted(info.keys()):
                        value = info[key]
                        if value is not None:  # Only write non-null values
                            f.write(f"  {key}: {value}\n")
                    f.write("\n")
        
        print(f"Element information has been saved to {filename}")
        
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
            
            input("\nPress Enter to continue...")
        
        # Remove highlights when done
        await remove_highlights(page)
        
        input("\nPress Enter to close the browser...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 