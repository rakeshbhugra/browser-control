from src.interfaces.tool_response import ToolResponse
from src.interfaces.context import Context
import traceback
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

async def goto_page_tool(url: str, context: Context) -> ToolResponse:
    try:
        print(f"Navigating to URL: {url}")
        # Continue with whatever we have after 5 seconds, don't wait for full load
        await context.page.goto(url, timeout=5000, wait_until='domcontentloaded')
        return ToolResponse(
            text_response = f"Navigation completed, Now we're on {url}",
            tool_output = "",
            tool_worked = True
        )
    except Exception as e:
        return ToolResponse(
            text_response = f'{traceback.format_exc()}',
            tool_output = "",
            tool_worked = False
        )