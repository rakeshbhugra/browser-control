from src.interfaces.tool_response import ToolResponse

async def task_complete_tool() -> ToolResponse:
    # Signal that the task is complete
    print("Task marked as complete")
    message = "Task has been marked as complete."
    return ToolResponse(text_response=message, tool_output=message) 