from src.interfaces.tool_response import ToolResponse
from src.interfaces.context import Context
import traceback

async def input_to_element_tool(text: str, locator: str, context: Context) -> ToolResponse:
    try:
        await context.page.locator(locator).fill(text)
        return ToolResponse(
            text_response=f"Added {text} to {locator}",
            tool_output=text,
            tool_worked=True
        )
    except Exception as e:
        return ToolResponse(text_response=f"{traceback.format_exc()}", tool_output="", tool_worked=False)
