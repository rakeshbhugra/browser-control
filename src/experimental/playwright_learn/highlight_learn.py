"""
Module for highlighting elements in a webpage using Playwright.
"""

import base64
from typing import Optional

from playwright.async_api import Page


async def highlight_page(page: Page) -> str:
    """
    Reads a webpage and highlights clickable elements with bounding boxes.
    
    Args:
        query: The URL or HTML content to process
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

        // Find and highlight clickable elements
        const clickableElements = document.querySelectorAll('button, a, input, select, [role="button"], [onclick]');
        clickableElements.forEach((element, index) => {
            highlightElement(element, index);
        });
    """)

    # Take a screenshot of the page with highlights
    screenshot = await page.screenshot(full_page=True)
    return base64.b64encode(screenshot).decode('utf-8')


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
    """) 