
import base64
from playwright.async_api import Page
from pydantic import BaseModel
from typing import Optional, Dict

class DrawBoundingBoxesAroundElementsResponse(BaseModel):
    screenshot: Optional[str] = None
    element_index_dict: dict

async def draw_bounding_boxes_around_elements(page: Page, need_screenshot: bool = True) -> DrawBoundingBoxesAroundElementsResponse:
    """
    Reads a webpage and highlights clickable elements with bounding boxes.
    Also stores element information for later clicking.
    
    Args:
        page: The Playwright Page object
        
    Returns:
        DrawBoundingBoxesAroundElementsResponse: screenshot of the page with highlights
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
    if need_screenshot:
        screenshot = await page.screenshot(full_page=True)
        screenshot = base64.b64encode(screenshot).decode('utf-8')
    else:
        screenshot = None

    element_index_dict = await get_element_index_dict(page)
    return DrawBoundingBoxesAroundElementsResponse(
        screenshot=screenshot,
        element_index_dict=element_index_dict
        )

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


async def get_element_index_dict(page: Page) -> dict:
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
    return element_index