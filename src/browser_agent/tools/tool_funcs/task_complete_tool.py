from src.interfaces.tool_response import ToolResponse
from src.utils.print_helper import print_helper
from src.interfaces.context import Context

async def task_complete_tool(context: Context) -> ToolResponse:
    # Signal that the task is complete
    print_helper.green_print("Task marked as complete")
    message = "Task has been marked as complete."
    # exit the program
    exit()
    return ToolResponse(text_response=message, tool_output=message) 