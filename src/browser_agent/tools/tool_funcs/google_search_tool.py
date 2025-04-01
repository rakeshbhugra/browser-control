from src.interfaces.tool_response import ToolResponse
from src.interfaces.context import Context
import traceback

async def google_search_tool(query: str, context: Context) -> ToolResponse:
    try:
        print(f"Searching Google for: {query}")
        
        await context.page.goto("https://www.bing.com")
        await context.page.wait_for_timeout(1000)
        await context.page.fill("textarea", query)
        await context.page.keyboard.press("Enter")
        await context.page.wait_for_timeout(1000)

        return ToolResponse(
            text_response = f"google searched for {query}, now on search results page",
            tool_output = "",
            tool_worked = True
        )
    
    except Exception as e:
        return ToolResponse(
            text_response = f'{traceback.format_exc()}',
            tool_output = "",
            tool_worked = False
        )
        