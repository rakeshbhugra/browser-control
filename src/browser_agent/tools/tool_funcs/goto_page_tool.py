from src.interfaces.tool_response import ToolResponse
from src.interfaces.context import Context
import traceback

async def goto_page_tool(url: str, context: Context) -> ToolResponse:
    try:
        await context.page.goto(url)
        print(f"Navigating to URL: {url}")
        return ToolResponse(
            text_response = f"Navigated to {url}",
            tool_output = "",
            tool_worked = True
        )
    except Exception as e:
        return ToolResponse(
            text_response = f'{traceback.format_exc()}',
            tool_output = "",
            tool_worked = False
        )