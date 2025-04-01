from src.interfaces.tool_response import ToolResponse
from src.interfaces.context import Context
import traceback

async def click_element_tool(locator: str, context: Context) -> ToolResponse:
    try:
        await context.page.locator(locator).click()
        return ToolResponse(
            text_response = f"Clicked on element with locator: {locator}",
            tool_output = "",
            tool_worked = True
        )
    except Exception as e:
        return ToolResponse(
            text_response = f'{traceback.format_exc()}',
            tool_output = "",
            tool_worked = False
        )