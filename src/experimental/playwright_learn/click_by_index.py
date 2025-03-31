"""
Module for highlighting elements and clicking them by index in a webpage using Playwright.
"""

import base64
from typing import Optional, List, Dict
from playwright.async_api import Page

async def highlight_page(page: Page) -> str:
    """
    Reads a webpage and highlights clickable elements with bounding boxes.
    Also stores element information for later clicking.
    
    Args:
        page: The Playwright Page object
        
    Returns:
        str: Base64 encoded screenshot of the page with highlights
    """
    # First, inject the highlight container and styles
    await page.evaluate("""
        // Create highlight container if it doesn't exist
        let container = document.getElementById('playwright-highlight-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'playwright-highlight-container';
            container.style.position = 'fixed';
            container.style.pointerEvents = 'none';
            container.style.top = '0';
            container.style.left = '0';
            container.style.width = '100%';
            container.style.height = '100%';
            container.style.zIndex = '2147483647';
            document.body.appendChild(container);
        }

        // Define colors for different element types
        const colors = {
            'button': '#FF0000',  // Red
            'a': '#00FF00',       // Green
            'input': '#0000FF',   // Blue
            'select': '#FFA500',  // Orange
            'textarea': '#800080', // Purple
            'default': '#800080'  // Purple
        };

        // Function to highlight an element
        function highlightElement(element, index) {
            const rect = element.getBoundingClientRect();
            const tagName = element.tagName.toLowerCase();
            const color = colors[tagName] || colors.default;
            const backgroundColor = color + '1A'; // 10% opacity

            // Create highlight overlay
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.border = `2px solid ${color}`;
            overlay.style.backgroundColor = backgroundColor;
            overlay.style.pointerEvents = 'none';
            overlay.style.boxSizing = 'border-box';
            overlay.style.top = `${rect.top}px`;
            overlay.style.left = `${rect.left}px`;
            overlay.style.width = `${rect.width}px`;
            overlay.style.height = `${rect.height}px`;

            // Create label
            const label = document.createElement('div');
            label.className = 'playwright-highlight-label';
            label.style.position = 'fixed';
            label.style.background = color;
            label.style.color = 'white';
            label.style.padding = '1px 4px';
            label.style.borderRadius = '4px';
            label.style.fontSize = `${Math.min(12, Math.max(8, rect.height / 2))}px`;
            label.textContent = index;

            const labelWidth = 20;
            const labelHeight = 16;

            let labelTop = rect.top + 2;
            let labelLeft = rect.left + rect.width - labelWidth - 2;

            if (rect.width < labelWidth + 4 || rect.height < labelHeight + 4) {
                labelTop = rect.top - labelHeight - 2;
                labelLeft = rect.left + rect.width - labelWidth;
            }

            label.style.top = `${labelTop}px`;
            label.style.left = `${labelLeft}px`;

            container.appendChild(overlay);
            container.appendChild(label);
        }

        // Find and highlight clickable elements and input fields
        const elements = document.querySelectorAll('button, a, input, select, textarea, [role="button"], [onclick]');
        window.highlightedElements = Array.from(elements);
        elements.forEach((element, index) => {
            highlightElement(element, index);
        });
    """)

    # Take a screenshot of the page with highlights
    screenshot = await page.screenshot(full_page=True)
    return base64.b64encode(screenshot).decode('utf-8')

async def get_element_info(page: Page, index: int) -> Dict:
    """
    Get information about a highlighted element by its index.
    
    Args:
        page: The Playwright Page object
        index: The index of the element to get information about
        
    Returns:
        Dict containing information about the element
    """
    info = await page.evaluate("""
        (index) => {
            const element = window.highlightedElements[index];
            if (!element) return null;
            
            const tagName = element.tagName.toLowerCase();
            const isInput = tagName === 'input' || tagName === 'textarea';
            
            return {
                tagName: tagName,
                text: element.textContent.trim(),
                type: element.type || null,
                id: element.id || null,
                className: element.className || null,
                href: element.href || null,
                value: element.value || null,
                placeholder: element.placeholder || null,
                isInput: isInput,
                inputType: isInput ? element.type || 'text' : null,
                isPassword: isInput && element.type === 'password',
                isSelect: tagName === 'select',
                isButton: tagName === 'button' || element.getAttribute('role') === 'button',
                isLink: tagName === 'a'
            };
        }
    """, index)
    
    return info

async def click_element(page: Page, index: int) -> bool:
    """
    Click a highlighted element by its index.
    
    Args:
        page: The Playwright Page object
        index: The index of the element to click
        
    Returns:
        bool: True if click was successful, False otherwise
    """
    success = await page.evaluate("""
        (index) => {
            const element = window.highlightedElements[index];
            if (!element) return false;
            
            try {
                element.click();
                return true;
            } catch (e) {
                return false;
            }
        }
    """, index)
    
    return success

async def fill_input(page: Page, index: int, text: str) -> bool:
    """
    Fill text into an input element by its index using smart input handling.
    
    Args:
        page: The Playwright Page object
        index: The index of the element to fill
        text: The text to fill into the input
        
    Returns:
        bool: True if fill was successful, False otherwise
    """
    try:
        # First get element info and determine input strategy
        element_info = await page.evaluate("""(index) => {
            const element = window.highlightedElements[index];
            if (!element) return null;
            
            return {
                isContentEditable: element.isContentEditable,
                isDisabled: element.disabled || element.readOnly,
                tagName: element.tagName.toLowerCase(),
                inputType: element.type || 'text',
                isRichText: element.getAttribute('role') === 'textbox' || 
                           element.classList.contains('rich-text') ||
                           element.classList.contains('editor'),
                value: element.value || element.textContent,
                selector: (() => {
                    // Try to get unique selector
                    if (element.id) return '#' + element.id;
                    if (element.name) return `[name="${element.name}"]`;
                    
                    // Try aria-label
                    const ariaLabel = element.getAttribute('aria-label');
                    if (ariaLabel) return `[aria-label="${ariaLabel}"]`;
                    
                    // Try placeholder
                    const placeholder = element.getAttribute('placeholder');
                    if (placeholder) return `[placeholder="${placeholder}"]`;
                    
                    // Generate path selector
                    let path = [];
                    let el = element;
                    while (el) {
                        let selector = el.tagName.toLowerCase();
                        if (el.className) {
                            const classes = Array.from(el.classList).join('.');
                            if (classes) selector += '.' + classes;
                        }
                        path.unshift(selector);
                        el = el.parentElement;
                    }
                    return path.join(' > ');
                })()
            };
        }""", {"index": index})

        if not element_info:
            print("Element not found")
            return False

        if element_info["isDisabled"]:
            print("Element is disabled or readonly")
            return False

        # Get locator for the element
        locator = page.locator(element_info["selector"])

        # Wait for element to be ready
        await locator.wait_for(state="visible")

        # Clear existing content first
        if element_info["value"]:
            if element_info["isContentEditable"] or element_info["isRichText"]:
                await locator.evaluate("el => el.textContent = ''")
            else:
                await locator.fill("")
                await page.wait_for_timeout(100)  # Small delay after clearing

        # Choose input method based on element type
        if element_info["isContentEditable"] or element_info["isRichText"]:
            # Use type for contenteditable and rich text editors
            await locator.type(text, delay=50)  # Add slight delay between keystrokes
        elif element_info["tagName"] == "textarea":
            # Use type for textarea to preserve newlines
            await locator.type(text, delay=20)
        else:
            # Use fill for standard input fields
            await locator.fill(text)

        # Verify the input was successful
        actual_value = await locator.evaluate("""el => {
            return el.isContentEditable ? el.textContent : el.value;
        }""")
        
        if not actual_value or text not in actual_value:
            print(f"Input verification failed. Expected: {text}, Got: {actual_value}")
            return False

        return True

    except Exception as e:
        print(f"Error filling input: {e}")
        return False

async def remove_highlights(page: Page) -> None:
    """
    Removes all highlight overlays and labels from the page.
    
    Args:
        page: The Playwright Page object
    """
    await page.evaluate("""
        // Remove the highlight container and all its contents
        const container = document.getElementById('playwright-highlight-container');
        if (container) {
            container.remove();
        }
        // Clear the stored elements
        window.highlightedElements = [];
    """) 